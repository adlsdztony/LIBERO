#!/usr/bin/env python3

import argparse
import cv2
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

import libero.libero.envs.bddl_utils as BDDLUtils
from libero.libero.envs import *

# Import our motion planning adapter
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libero_adapter import LiberoMPLibAdapter, create_libero_planner


def collect_scripted_trajectory(
    env, planner, target_joint_positions, target_grippers, remove_directory=[]
):
    """
    Simple joint position tracking demonstration collection using waypoints.
    """

    reset_success = False
    while not reset_success:
        try:
            env.reset()
            reset_success = True
        except:
            continue

    env.render()

    task_completion_hold_count = -1
    saving = True
    count = 0
    joint_index = 0

    print(f"🤖 Starting automated trajectory with {len(target_joint_positions)} waypoints")

    # Run multiple empty actions to ensure the arm is stable
    empty_action = np.zeros(8)
    num_stabilize_steps = 100
    for _ in range(num_stabilize_steps):
        obs, _, _, _ = env.step(empty_action)
        current_joints = planner.get_current_joint_positions(obs)
        current_gripper = planner.get_gripper_joint_positions(obs)
        env.render()

    while joint_index < len(target_joint_positions):
        # Get current joint positions from observation
        current_joints = planner.get_current_joint_positions(obs)
        current_gripper = planner.get_gripper_joint_positions(obs)

        # Get target joint positions
        target_joints = target_joint_positions[joint_index]
        target_gripper = target_grippers[joint_index]

        print(f"📍 Waypoint {joint_index + 1}/{len(target_joint_positions)}: Moving to joint configuration")
        print(f"   Target joints: {[f'{x:.3f}' for x in target_joints]}")
        print(f"   Target gripper: {target_gripper}")

        # Plan trajectory to target joint position using motion planner
        result = planner.planner.plan_qpos(
            goal_qposes=[target_joints], 
            current_qpos=np.concatenate((current_joints, current_gripper)),
            time_step=0.1,
            rrt_range=0.1,
            planning_time=5.0,
            fix_joint_limits=True,
            verbose=False
        )
        if result["status"] != "Success":
            print(f"❌ Motion planning failed: {result['status']}, skipping this waypoint")
            joint_index += 1
            continue

        # Add several duplicate steps to hold the final position
        duplicate_steps = 20
        if len(result["position"]) == 0:
            result["position"] = np.array([target_joints] * (duplicate_steps))
        else:
            last_step = result["position"][-1]
            result["position"] = np.concatenate(
                [result["position"], np.tile(last_step, (duplicate_steps, 1))], axis=0
            )
        
        # Execute the planned joint trajectory
        total_steps = result["position"].shape[0]
        print(f"   Executing trajectory with {total_steps} steps")

        for i in range(total_steps):
            count += 1

            # Get planned joint positions for this step
            planned_joints = result["position"][i]
            current_joints = planner.get_current_joint_positions(obs)
            joint_error = planned_joints - current_joints

            step = 3
            
            for j in range(step):
                action = np.zeros(8)
                action[:7] = joint_error  # Joint position control
                action[7] = target_gripper  # Set gripper action
                
                # Step the environment
                obs, reward, done, info = env.step(action)
                env.render()

            # Check for task completion
            if task_completion_hold_count == 0:
                print("🎯 Task completed!")
                break

            # State machine to check for having a success for 10 consecutive timesteps
            if env._check_success():
                if task_completion_hold_count > 0:
                    task_completion_hold_count -= 1
                else:
                    task_completion_hold_count = 10
                    print("✅ Task success detected, holding for 10 timesteps")
            else:
                task_completion_hold_count = -1

            time.sleep(0.01)
        
        # Calculate final joint error
        final_joints = planner.get_current_joint_positions(obs)
        joint_error_final = target_joints - final_joints
        print(f"   Final joint error: {[f'{e:.3f}' for e in joint_error_final]}")

        # Move to next joint target
        joint_index += 1
        
        # If task completed, break
        if task_completion_hold_count == 0:
            break

    print(f"🏁 Automation completed with {count} total steps")
    
    # cleanup for end of data collection episodes
    if not saving:
        remove_directory.append(env.ep_directory.split("/")[-1])
    
    env.close()
    return saving


def load_waypoints_from_hdf5(waypoints_file):
    """
    Load waypoints from HDF5 file created by collect_waypoints.py
    
    Args:
        waypoints_file (str): Path to the waypoints HDF5 file
        
    Returns:
        dict: Dictionary containing waypoint data for all demonstrations
    """
    waypoints_data = {}
    
    try:
        with h5py.File(waypoints_file, "r") as f:
            print(f"📁 HDF5 file opened successfully: {waypoints_file}")
            print(f"📁 Root keys: {list(f.keys())}")
            
            if "data" not in f:
                print("❌ No 'data' group found in HDF5 file")
                return {"demonstrations": []}
                
            data_group = f["data"]
            print(f"📁 Data group keys: {list(data_group.keys())}")
            
            # Load metadata
            waypoints_data["metadata"] = {
                "date": data_group.attrs.get("date", ""),
                "time": data_group.attrs.get("time", ""),
                "problem_info": json.loads(data_group.attrs.get("problem_info", "{}")),
                "bddl_file_name": data_group.attrs.get("bddl_file_name", ""),
            }
            
            # Load all demonstrations
            waypoints_data["demonstrations"] = []
            demo_keys = [key for key in data_group.keys() if key.startswith("demo_")]
            print(f"📁 Found demo keys: {demo_keys}")
            
            if not demo_keys:
                print("❌ No demonstration keys found (keys starting with 'demo_')")
                return waypoints_data
            
            for demo_key in sorted(demo_keys):
                demo_group = data_group[demo_key]
                demo_datasets = list(demo_group.keys())
                print(f"📁 {demo_key} datasets: {demo_datasets}")
                
                demo_data = {
                    "joint_positions": np.array(demo_group["joint_positions"]),
                    "ee_pos_quat": np.array(demo_group["ee_pos_quat"]),
                    "gripper_commands": np.array(demo_group.get("gripper_commands", demo_group.get("gripper_pos", []))),
                }
                print(f"📁 {demo_key} waypoint shapes: joint_positions={demo_data['joint_positions'].shape}, "
                      f"ee_pos_quat={demo_data['ee_pos_quat'].shape}, gripper_commands={demo_data['gripper_commands'].shape}")
                waypoints_data["demonstrations"].append(demo_data)
            
            print(f"✅ Successfully loaded {len(waypoints_data['demonstrations'])} demonstrations")
    
    except Exception as e:
        print(f"❌ Error loading waypoints file: {e}")
        return {"demonstrations": []}
    
    return waypoints_data


def find_waypoints_file(waypoints_directory, problem_name, language_instruction):
    """
    Find the most recent waypoints file for the given task.
    
    Args:
        waypoints_directory (str): Directory containing waypoint files
        problem_name (str): Problem name
        language_instruction (str): Language instruction
        
    Returns:
        str: Path to the waypoints file, or None if not found
    """
    if not os.path.exists(waypoints_directory):
        print(f"⚠️ Waypoints directory does not exist: {waypoints_directory}")
        return None
    
    # Look for directories matching the pattern
    instruction_slug = language_instruction.replace(" ", "_").strip('""')
    
    matching_dirs = []
    for item in os.listdir(waypoints_directory):
        item_path = os.path.join(waypoints_directory, item)
        if os.path.isdir(item_path):
            # Check if directory name contains both problem name and instruction
            if problem_name in item and instruction_slug in item:
                matching_dirs.append(item_path)
    
    if not matching_dirs:
        print(f"⚠️ No matching waypoint directories found")
        print(f"   Problem: {problem_name}")
        print(f"   Instruction: {instruction_slug}")
        print(f"   Available directories in {waypoints_directory}:")
        try:
            for item in os.listdir(waypoints_directory):
                if os.path.isdir(os.path.join(waypoints_directory, item)):
                    print(f"     - {item}")
        except:
            print(f"     (could not list directory)")
        return None
    
    # Find the most recent directory (sort by modification time)
    latest_dir = max(matching_dirs, key=lambda x: os.path.getmtime(x))
    
    # Look for waypoints.hdf5 file in the directory
    waypoints_file = os.path.join(latest_dir, "waypoints.hdf5")
    if os.path.exists(waypoints_file):
        return waypoints_file
    
    print(f"⚠️ waypoints.hdf5 not found in {latest_dir}")
    return None


def gather_demonstrations_as_hdf5(
    directory, out_dir, env_info, args, remove_directory=[]
):
    """
    Gathers the demonstrations saved in @directory into a
    single hdf5 file.
    (Same as original function)
    """
    hdf5_path = os.path.join(out_dir, "demo.hdf5")
    f = h5py.File(hdf5_path, "w")

    # store some metadata in the attributes of one group
    grp = f.create_group("data")

    num_eps = 0
    env_name = None  # will get populated at some point

    for ep_directory in os.listdir(directory):
        if ep_directory in remove_directory:
            continue
        state_paths = os.path.join(directory, ep_directory, "state_*.npz")
        states = []
        actions = []

        for state_file in sorted(glob(state_paths)):
            dic = np.load(state_file, allow_pickle=True)
            env_name = str(dic["env"])

            states.extend(dic["states"])
            for ai in dic["action_infos"]:
                actions.append(ai["actions"])

        if len(states) == 0:
            continue

        # Delete the first actions and the last state
        del states[-1]
        assert len(states) == len(actions)

        num_eps += 1
        ep_data_grp = grp.create_group("demo_{}".format(num_eps))

        # store model xml as an attribute
        xml_path = os.path.join(directory, ep_directory, "model.xml")
        with open(xml_path, "r") as f:
            xml_str = f.read()
        ep_data_grp.attrs["model_file"] = xml_str

        # write datasets for states and actions
        ep_data_grp.create_dataset("states", data=np.array(states))
        ep_data_grp.create_dataset("actions", data=np.array(actions))

    # write dataset attributes (metadata)
    now = datetime.datetime.now()
    grp.attrs["date"] = "{}-{}-{}".format(now.month, now.day, now.year)
    grp.attrs["time"] = "{}:{}:{}".format(now.hour, now.minute, now.second)
    grp.attrs["repository_version"] = suite.__version__
    grp.attrs["env"] = env_name
    grp.attrs["env_info"] = env_info

    grp.attrs["problem_info"] = json.dumps(problem_info)
    grp.attrs["bddl_file_name"] = args.bddl_file
    grp.attrs["bddl_file_content"] = str(open(args.bddl_file, "r", encoding="utf-8"))

    f.close()


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="Auto collect demonstrations using waypoints")
    parser.add_argument(
        "--bddl-file", 
        type=str, 
        default="libero/libero/bddl_files/libero_90/KITCHEN_SCENE1_open_the_bottom_drawer_of_the_cabinet.bddl",
        help="BDDL task file (default: kitchen drawer opening task)"
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="demonstration_data/auto_demo",
        help="Output directory for demonstrations"
    )
    parser.add_argument(
        "--waypoints-directory",
        type=str,
        default="demonstration_data/waypoints",
        help="Directory containing waypoint files"
    )
    parser.add_argument(
        "--waypoint-type",
        type=str,
        default="joint_position",
        choices=["joint_position"],
        help="Type of waypoints to use (only joint_position supported for now)"
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
    parser.add_argument(
        "--num-demonstration",
        type=int,
        default=5,
        help="Number of demonstrations to collect",
    )
    
    # Motion planning specific arguments
    parser.add_argument(
        "--urdf-path", 
        type=str, 
        default="./data/panda/panda.urdf",
        help="Path to robot URDF file"
    )
    parser.add_argument(
        "--srdf-path", 
        type=str, 
        default="./data/panda/panda.srdf",
        help="Path to robot SRDF file"
    )

    args = parser.parse_args()

    # Fixed robot configuration for auto collection
    robots = ["Panda"]
    
    # Get controller config (JOINT_POSITION for automation)
    controller_config = load_controller_config(default_controller="JOINT_POSITION")
    controller_config["kp"] = 300.0
    controller_config["damping_ratio"] = 0.8
    controller_config["output_max"] = 0.5
    controller_config["output_min"] = -0.5

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
    
    # Find waypoints file
    waypoints_file = find_waypoints_file(args.waypoints_directory, problem_name, language_instruction)
    if not waypoints_file:
        print(f"❌ No waypoints file found for task: {language_instruction}")
        print(f"   Searched in: {args.waypoints_directory}")
        print(f"   Expected pattern: *{problem_name}*{language_instruction.replace(' ', '_')}*/waypoints.hdf5")
        exit(1)
    
    print(f"📁 Using waypoints from: {waypoints_file}")
    
    # Load waypoints
    waypoints_data = load_waypoints_from_hdf5(waypoints_file)
    if not waypoints_data["demonstrations"]:
        print("❌ No waypoint demonstrations found in file")
        exit(1)
    
    # Use the first demonstration's waypoints (you could extend this to use all)
    demo_waypoints = waypoints_data["demonstrations"][0]
    target_joint_positions = demo_waypoints["joint_positions"]
    
    # Convert gripper commands to robot actions
    # gripper_commands contains True (close) or False (open)
    target_grippers = []
    if "gripper_commands" in demo_waypoints:
        # New format: direct boolean commands
        for gripper_command in demo_waypoints["gripper_commands"]:
            target_grippers.append(1 if gripper_command else -1)  # 1=close, -1=open
        print(f"📍 Using new gripper command format")
    elif "gripper_pos" in demo_waypoints:
        # Legacy format: convert from positions
        print(f"📍 Converting from legacy gripper position format")
        gripper_threshold = 0.02
        for gripper_pos in demo_waypoints["gripper_pos"]:
            # Average gripper position (both fingers)
            avg_gripper_pos = np.mean(gripper_pos)
            target_grippers.append(-1 if avg_gripper_pos > gripper_threshold else 1)
    else:
        print("❌ No gripper data found in waypoints")
        exit(1)
    
    print(f"📍 Loaded {len(target_joint_positions)} waypoints from demonstration")
    print(f"🤏 Gripper commands: {['CLOSE' if cmd == 1 else 'OPEN' for cmd in target_grippers]}")
    print(f"💾 Demonstrations will be saved to: {args.directory}")
    
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

    # Wrap with visualization wrapper
    env = VisualizationWrapper(env)

    # Grab reference to controller config and convert it to json-encoded string
    env_info = json.dumps(config)

    # Create motion planner
    try:
        planner = LiberoMPLibAdapter(
            urdf_path=args.urdf_path,
            srdf_path=args.srdf_path,
            move_group="panda_hand"
        )
        print("🤖 Motion planner initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize motion planner: {e}")
        print("Please check URDF/SRDF paths and ensure mplib is installed")
        exit(1)

    # Set the transform from the world to the robot base
    KITCHEN_SCENE_ROBOT_BASE_POS = [-0.66, 0, 0.804]
    planner.set_base_pose(KITCHEN_SCENE_ROBOT_BASE_POS, [0, 0, 0, 1])

    # Extract timestamp from waypoints file for consistent naming
    waypoints_timestamp = os.path.basename(os.path.dirname(waypoints_file)).split('_')[3:5]
    timestamp_str = "_".join(waypoints_timestamp)

    # wrap the environment with data collection wrapper
    tmp_directory = "demonstration_data/tmp/{}_ln_{}_auto/{}".format(
        problem_name,
        language_instruction.replace(" ", "_").strip('""'),
        timestamp_str,
    )

    env = DataCollectionWrapper(env, tmp_directory)

    # make a new timestamped directory for output
    new_dir = os.path.join(
        args.directory,
        f"{domain_name}_ln_{problem_name}_{timestamp_str}_auto_"
        + language_instruction.replace(" ", "_").strip('""'),
    )

    # handle the case when the directory name is too long
    if len(new_dir) > 200:
        new_dir = os.path.join(
            args.directory,
            f"{domain_name}_ln_{problem_name}_{timestamp_str}_auto_"
            + language_instruction.replace(" ", "_").strip('""')[:180 - len(timestamp_str)],
        )

    os.makedirs(new_dir, exist_ok=True)

    # collect demonstrations
    remove_directory = []
    i = 0
    while i < args.num_demonstration:
        print(f"\n🔄 Collecting automated demonstration {i+1}/{args.num_demonstration}")
        saving = collect_scripted_trajectory(
            env, planner, target_joint_positions, target_grippers, remove_directory
        )
        if saving:
            gather_demonstrations_as_hdf5(
                tmp_directory, new_dir, env_info, args, remove_directory
            )
            i += 1
            print(f"✅ Successfully collected demonstration {i}")
        else:
            print("❌ Failed to collect demonstration, retrying...")
    
    print(f"\n🎉 Auto collection completed! {i} demonstrations saved to {new_dir}")
