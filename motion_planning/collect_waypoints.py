import argparse
import datetime
import h5py
import scripts.init_path
import json
import numpy as np
import os
import robosuite as suite
import time
from glob import glob
from robosuite import load_controller_config
from robosuite.wrappers import DataCollectionWrapper, VisualizationWrapper
from robosuite.utils.input_utils import input2action

import libero.libero.envs.bddl_utils as BDDLUtils
from libero.libero.envs import *
from waypoint_keyboard import WaypointKeyboard

def collect_waypoint_trajectory(
    env, device, arm, env_configuration, problem_info
):
    """
    Use the keyboard to collect waypoints demonstration.
    The waypoints are saved as joint positions, end effector poses, and gripper positions.

    Args:
        env (MujocoEnv): environment to control
        device (WaypointKeyboard): keyboard device for control and waypoint recording
        arm (str): which arm to control (eg bimanual) 'right' or 'left'
        env_configuration (str): specified environment configuration
        problem_info (dict): problem information from BDDL file
    """

    reset_success = False
    while not reset_success:
        try:
            env.reset()
            reset_success = True
        except:
            continue

    env.render()

    task_completion_hold_count = -1  # counter to collect 10 timesteps after reaching goal
    device.start_control()

    # Loop until we get a reset from the input or the task completes
    saving = True
    count = 0
    waypoint_count = 0
    last_waypoint_step = -1  # Track when the last waypoint was recorded
    
    # Storage for waypoints
    waypoints_data = {
        'joint_positions': [],
        'ee_pos_quat': [],
        'gripper_commands': []  # Store user commands (True=close, False=open) instead of positions
    }

    print("🎮 Starting waypoint collection. Press 'J' to record waypoints!")

    while True:
        count += 1

        # Set active robot
        active_robot = (
            env.robots[0]
            if env_configuration == "bimanual"
            else env.robots[arm == "left"]
        )

        # Get the newest action and check for waypoint recording
        action, grasp = input2action(
            device=device,
            robot=active_robot,
            active_arm=arm,
            env_configuration=env_configuration,
        )

        # If action is none, then this a reset so we should break
        if action is None:
            print("🛑 Collection stopped by user")
            saving = False
            break

        # Run environment step
        obs, _, _, _ = env.step(action)
        
        # Check if waypoint recording was requested (more efficient check)
        if device.record_waypoint:
            waypoint_count += 1
            last_waypoint_step = count  # Track when this waypoint was recorded
            
            # Reset the flag immediately to avoid duplicate recordings
            device.record_waypoint = False
            
            # Extract waypoint data
            joint_pos = obs["robot0_joint_pos"].copy()
            ee_pos = obs["robot0_eef_pos"].copy()
            ee_quat = obs["robot0_eef_quat"].copy()
            gripper_command = device.grasp  # Store user's gripper command (True=close, False=open)
            
            # Store waypoint data
            waypoints_data['joint_positions'].append(joint_pos)
            waypoints_data['ee_pos_quat'].append(np.concatenate([ee_pos, ee_quat]))
            waypoints_data['gripper_commands'].append(gripper_command)
            
            print(f"✅ Waypoint {waypoint_count} recorded!")
            print(f"   Joint positions: {[f'{x:.3f}' for x in joint_pos]}")
            print(f"   EE position: {[f'{x:.3f}' for x in ee_pos]}")
            print(f"   Gripper command: {'CLOSE' if gripper_command else 'OPEN'}")
            print()

        env.render()

        if task_completion_hold_count == 0:
            print("🎯 Task completed!")
            break

        # state machine to check for having a success for 10 consecutive timesteps
        if env._check_success():
            if task_completion_hold_count > 0:
                task_completion_hold_count -= 1  # latched state, decrement count
            else:
                task_completion_hold_count = 10  # reset count on first success timestep
                
                # Auto-record final waypoint if not already recorded in the last few steps
                # This ensures we always capture the successful end state
                auto_record_final = True
                if waypoint_count > 0:
                    # Check if a waypoint was recorded recently (within last 20 timesteps)
                    # If so, we don't need to auto-record
                    recent_waypoint_threshold = 20
                    if count - last_waypoint_step <= recent_waypoint_threshold:
                        auto_record_final = False
                
                if auto_record_final:
                    waypoint_count += 1
                    
                    # Extract waypoint data
                    joint_pos = obs["robot0_joint_pos"].copy()
                    ee_pos = obs["robot0_eef_pos"].copy()
                    ee_quat = obs["robot0_eef_quat"].copy()
                    gripper_command = device.grasp  # Store user's gripper command at task completion
                    
                    # Store waypoint data
                    waypoints_data['joint_positions'].append(joint_pos)
                    waypoints_data['ee_pos_quat'].append(np.concatenate([ee_pos, ee_quat]))
                    waypoints_data['gripper_commands'].append(gripper_command)
                    
                    print(f"🎯 Auto-recorded final waypoint {waypoint_count} at task success!")
                    print(f"   Joint positions: {[f'{x:.3f}' for x in joint_pos]}")
                    print(f"   EE position: {[f'{x:.3f}' for x in ee_pos]}")
                    print(f"   Gripper command: {'CLOSE' if gripper_command else 'OPEN'}")
                    print()
                    
                    last_waypoint_step = count
        else:
            task_completion_hold_count = -1  # null the counter if there's no success

    print(f"📊 Total waypoints collected: {waypoint_count}")
    
    # Always save waypoints if any were collected, even if task wasn't completed
    if waypoint_count > 0:
        saving = True
    else:
        print("⚠️  No waypoints collected!")
        saving = False

    env.close()
    return saving, waypoints_data if saving else None


def gather_waypoints_as_hdf5(
    out_dir, env_info, args, waypoints_data, problem_info
):
    """
    Saves the waypoints data directly to HDF5 file.
    
    The structure of the hdf5 file is as follows:
    
    data (group)
        date (attribute) - date of collection
        time (attribute) - time of collection
        repository_version (attribute) - repository version used during collection
        env (attribute) - environment name
        
        demo_1 (group) - waypoint demonstration
            joint_positions (dataset) - recorded joint positions at waypoints
            ee_pos_quat (dataset) - end effector position and quaternion at waypoints
            gripper_commands (dataset) - gripper commands at waypoints (True=close, False=open)
    """

    hdf5_path = os.path.join(out_dir, "waypoints.hdf5")
    
    # Check if file already exists and load existing data
    existing_demos = []
    if os.path.exists(hdf5_path):
        try:
            with h5py.File(hdf5_path, "r") as f:
                if "data" in f:
                    data_group = f["data"]
                    demo_keys = [key for key in data_group.keys() if key.startswith("demo_")]
                    for demo_key in sorted(demo_keys):
                        demo_group = data_group[demo_key]
                        existing_demos.append({
                            "joint_positions": np.array(demo_group["joint_positions"]),
                            "ee_pos_quat": np.array(demo_group["ee_pos_quat"]),
                            "gripper_commands": np.array(demo_group.get("gripper_commands", demo_group.get("gripper_pos", []))),
                        })
        except:
            pass  # If file is corrupted, start fresh
    
    # Create new HDF5 file
    with h5py.File(hdf5_path, "w") as f:
        # Create data group
        grp = f.create_group("data")
        
        # Add all existing demonstrations
        for i, demo_data in enumerate(existing_demos):
            demo_num = i + 1
            ep_data_grp = grp.create_group(f"demo_{demo_num}")
            ep_data_grp.create_dataset("joint_positions", data=demo_data['joint_positions'])
            ep_data_grp.create_dataset("ee_pos_quat", data=demo_data['ee_pos_quat'])
            ep_data_grp.create_dataset("gripper_commands", data=demo_data['gripper_commands'])
        
        # Add new demonstration
        demo_num = len(existing_demos) + 1
        ep_data_grp = grp.create_group(f"demo_{demo_num}")
        ep_data_grp.create_dataset("joint_positions", data=np.array(waypoints_data['joint_positions']))
        ep_data_grp.create_dataset("ee_pos_quat", data=np.array(waypoints_data['ee_pos_quat']))
        ep_data_grp.create_dataset("gripper_commands", data=np.array(waypoints_data['gripper_commands']))

        # Write dataset attributes (metadata)
        now = datetime.datetime.now()
        grp.attrs["date"] = "{}-{}-{}".format(now.month, now.day, now.year)
        grp.attrs["time"] = "{}:{}:{}".format(now.hour, now.minute, now.second)
        grp.attrs["repository_version"] = suite.__version__
        grp.attrs["env"] = "LIBERO"
        grp.attrs["env_info"] = env_info

        grp.attrs["problem_info"] = json.dumps(problem_info)
        grp.attrs["bddl_file_name"] = args.bddl_file
        grp.attrs["bddl_file_content"] = str(open(args.bddl_file, "r", encoding="utf-8").read())

    print(f"✅ Waypoints saved to {hdf5_path} (demo_{demo_num})")


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="Collect waypoints for robot demonstrations")
    parser.add_argument(
        "--bddl-file", 
        type=str, 
        default="libero/libero/bddl_files/libero_90/KITCHEN_SCENE1_open_the_bottom_drawer_of_the_cabinet.bddl",
        help="BDDL task file (default: kitchen drawer opening task)"
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="demonstration_data/waypoints",
        help="Output directory for waypoints"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="single-arm-opposed",
        help="Specified environment configuration if necessary",
    )
    parser.add_argument(
        "--arm",
        type=str,
        default="right",
        help="Which arm to control (eg bimanual) 'right' or 'left'",
    )
    parser.add_argument(
        "--camera",
        type=str,
        default="agentview",
        help="Which camera to use for collecting demos",
    )
    parser.add_argument("--device", type=str, default="keyboard", choices=["keyboard"], 
                       help="Input device (only keyboard supported)")
    parser.add_argument(
        "--pos-sensitivity",
        type=float,
        default=1.5,
        help="How much to scale position user inputs",
    )
    parser.add_argument(
        "--rot-sensitivity",
        type=float,
        default=1.0,
        help="How much to scale rotation user inputs",
    )
    parser.add_argument(
        "--num-demonstration",
        type=int,
        default=1,
        help="Number of waypoint demonstrations to collect",
    )

    args = parser.parse_args()

    # Fixed robot and controller configuration for waypoint collection
    robots = ["Panda"]
    controller = "OSC_POSE"
    
    # Get controller config
    controller_config = load_controller_config(default_controller=controller)

    # Create argument configuration
    config = {
        "robots": robots,
        "controller_configs": controller_config,
    }

    assert os.path.exists(args.bddl_file)
    problem_info = BDDLUtils.get_problem_info(args.bddl_file)
    
    # Create environment
    problem_name = problem_info["problem_name"]
    domain_name = problem_info["domain_name"]
    language_instruction = problem_info["language_instruction"]
    
    if "TwoArm" in problem_name:
        config["env_configuration"] = args.config
    
    print(f"🎯 Task: {language_instruction}")
    print(f"📁 Waypoints will be saved to: {args.directory}")
    
    env = TASK_MAPPING[problem_name](
        bddl_file_name=args.bddl_file,
        **config,
        has_renderer=True,
        has_offscreen_renderer=False,
        render_camera=args.camera,
        ignore_done=True,
        use_camera_obs=False,
        reward_shaping=True,
        control_freq=20,
    )

    # Wrap this with visualization wrapper
    env = VisualizationWrapper(env)

    # Grab reference to controller config and convert it to json-encoded string
    env_info = json.dumps(config)

    # No need for temporary directory since we save waypoints directly
    # Just use the device for keyboard input
    device = WaypointKeyboard(
        pos_sensitivity=args.pos_sensitivity, 
        rot_sensitivity=args.rot_sensitivity
    )
    env.viewer.add_keypress_callback(device.on_press)

    # make a new timestamped directory
    t1, t2 = str(time.time()).split(".")
    new_dir = os.path.join(
        args.directory,
        f"{domain_name}_ln_{problem_name}_{t1}_{t2}_"
        + language_instruction.replace(" ", "_").strip('""'),
    )

    # handle the case when the directory name is too long
    if len(new_dir) > 200:
        new_dir = os.path.join(
            args.directory,
            f"{domain_name}_ln_{problem_name}_{t1}_{t2}_"
            + language_instruction.replace(" ", "_").strip('""')[:200 - len(t1) - len(t2) - 20],
        )

    os.makedirs(new_dir, exist_ok=True)

    # collect waypoint demonstrations
    i = 0
    ep = 0
    
    try:
        while i < args.num_demonstration:
            success_rate = i / ep if ep > 0 else 0
            print(f"\n📊 Trials: {ep}, Successes: {i}, Success rate: {success_rate:.2f}")
            print(f"🎮 Starting waypoint collection {ep + 1}")
            
            saving, waypoints_data = collect_waypoint_trajectory(
                env, device, args.arm, args.config, problem_info
            )
            
            if saving and waypoints_data:
                gather_waypoints_as_hdf5(
                    new_dir, env_info, args, waypoints_data, problem_info
                )
                i += 1
                print(f"✅ Successfully collected waypoint demonstration {i}")
            else:
                print("❌ Waypoint collection failed or cancelled")
            ep += 1
    except KeyboardInterrupt:
        print("\n🛑 Collection interrupted by user (Ctrl+C)")
        # Since we save waypoints immediately, no need for additional handling
        pass
    
    print(f"\n🎉 Waypoint collection completed! {i} demonstrations saved to {new_dir}")
