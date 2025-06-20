#!/usr/bin/env python3

import argparse
import cv2
import datetime
import h5py
import init_path
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

# Import our motion planning adapter
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libero_adapter import LiberoMPLibAdapter, create_libero_planner


def collect_scripted_trajectory(
    env, planner, target_poses, remove_directory=[]
):
    """
    Simple motion planning demonstration collection.
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
    pose_index = 0

    print(f"Starting scripted trajectory with {len(target_poses)} target poses")

    # Get initial observation with empty action
    empty_action = np.zeros(8)
    obs, _, _, _ = env.step(empty_action)
    # print(obs)
    
    while pose_index < len(target_poses):
        # Get current joint positions from observation
        current_joints = planner.get_current_joint_positions(obs)

        # Get target pose
        target_pose = target_poses[pose_index]
        print(f"Planning to pose {pose_index + 1}/{len(target_poses)}: {target_pose}")

        # Plan trajectory to target pose
        result = planner.plan_to_pose(target_pose, current_joints, use_screw=True)

        if result["status"] != "Success":
            print(f"Planning failed with status: {result['status']}")
            # Try with RRT planner
            result = planner.plan_to_pose(target_pose, current_joints, use_screw=False)
            if result["status"] != "Success":
                print("RRT planning also failed, skipping this pose")
                pose_index += 1
                continue

        # Execute the planned trajectory
        n_steps = result["position"].shape[0]
        print(f"Executing trajectory with {n_steps} steps")

        for i in range(n_steps):
            count += 1


            # JOINT POSITION
            planned_joints = result["position"][i]
            print(f"Planned joints: {[f'{j:.3f}' for j in planned_joints]}")
            current_joints = planner.get_current_joint_positions(obs)
            print(f"Current joints: {[f'{j:.3f}' for j in obs['robot0_joint_pos']]}")
            action = np.zeros(8)
            # action[:7] = planned_joints
            action[:7] = planned_joints - current_joints

            # JOINT VELOCITY
            action = np.zeros(8)
            action[:7] = result["velocity"][i]

            print(f"Action to take: {[f'{a:.3f}' for a in action]}")
            
            # Step the environment
            obs, reward, done, info = env.step(action)

            env.render()

            # Check for task completion
            if task_completion_hold_count == 0:
                print("Task completed!")
                break

            # State machine to check for having a success for 10 consecutive timesteps
            if env._check_success():
                if task_completion_hold_count > 0:
                    task_completion_hold_count -= 1
                else:
                    task_completion_hold_count = 10
                    print("Task success detected, holding for 10 timesteps")
            else:
                task_completion_hold_count = -1

            time.sleep(0.01)

        # Move to next pose
        pose_index += 1
        
        # If task completed, break
        if task_completion_hold_count == 0:
            break

    print(f"Total steps: {count}")
    
    # cleanup for end of data collection episodes
    if not saving:
        remove_directory.append(env.ep_directory.split("/")[-1])
    
    env.close()
    return saving


def get_scripted_poses_for_task(problem_name, language_instruction):
    """
    Define scripted target poses for different tasks.
    You can customize this function based on your specific tasks.
    
    Args:
        problem_name: name of the problem
        language_instruction: language instruction for the task
        
    Returns:
        list: List of target poses [[x,y,z,qx,qy,qz,qw], ...]
    """
    
    # Default poses - modify these based on your tasks
    default_poses = [
        [0.4, 0.3, 0.12, 0, 1, 0, 0],
        [0.4, 0.3, 0.8, 0, 1, 0, 0],
    ]
    

    poses = default_poses
    
    print(f"Using {len(poses)} scripted poses for task: {language_instruction}")
    return poses


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        type=str,
        default="demonstration_data",
    )
    parser.add_argument(
        "--robots",
        nargs="+",
        type=str,
        default="Panda",
        help="Which robot(s) to use in the env",
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
        "--controller",
        type=str,
        default="OSC_POSE",
        help="Choice of controller. Can be 'IK_POSE' or 'OSC_POSE'",
    )
    parser.add_argument(
        "--num-demonstration",
        type=int,
        default=10,
        help="Number of demonstrations to collect",
    )
    parser.add_argument("--bddl-file", type=str, required=True)
    
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

    # Get controller config
    controller_config = load_controller_config(default_controller=args.controller)

    # Create argument configuration
    config = {
        "robots": args.robots,
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
    
    print(f"Task: {language_instruction}")
    
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
        print("Motion planner initialized successfully")
    except Exception as e:
        print(f"Failed to initialize motion planner: {e}")
        print("Please check URDF/SRDF paths and ensure mplib is installed")
        exit(1)

    # Get scripted poses for this task
    target_poses = get_scripted_poses_for_task(problem_name, language_instruction)

    # wrap the environment with data collection wrapper
    tmp_directory = "demonstration_data/tmp/{}_ln_{}_scripted/{}".format(
        problem_name,
        language_instruction.replace(" ", "_").strip('""'),
        str(time.time()).replace(".", "_"),
    )

    env = DataCollectionWrapper(env, tmp_directory)

    # make a new timestamped directory
    t1, t2 = str(time.time()).split(".")
    new_dir = os.path.join(
        args.directory,
        f"{domain_name}_ln_{problem_name}_{t1}_{t2}_scripted_"
        + language_instruction.replace(" ", "_").strip('""'),
    )

    # handle the case when the directory name is too long
    if len(new_dir) > 200:
        new_dir = os.path.join(
            args.directory,
            f"{domain_name}_ln_{problem_name}_{t1}_{t2}_scripted_"
            + language_instruction.replace(" ", "_").strip('""')[:180 - len(t1) - len(t2)],
        )

    os.makedirs(new_dir)

    # collect demonstrations
    remove_directory = []
    i = 0
    while i < args.num_demonstration:
        print(f"\n=== Collecting demonstration {i+1}/{args.num_demonstration} ===")
        saving = collect_scripted_trajectory(
            env, planner, target_poses, remove_directory
        )
        if saving:
            gather_demonstrations_as_hdf5(
                tmp_directory, new_dir, env_info, args, remove_directory
            )
            i += 1
            print(f"Successfully collected demonstration {i}")
        else:
            print("Failed to collect demonstration, retrying...")
