#!/usr/bin/env python3

import argparse
import json
import numpy as np
import os
import time
from glob import glob
import robosuite.utils.transform_utils as transform_utils

import libero.libero.envs.bddl_utils as BDDLUtils
from libero.libero.envs import *
from robosuite import load_controller_config
from robosuite.wrappers import VisualizationWrapper

# Import our motion planning adapter
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libero_adapter import LiberoMPLibAdapter


def end_effector_pose_control(env, planner: LiberoMPLibAdapter, target_poses, gripper_commands, max_steps=5000):
    """
    Test end-effector pose control by commanding the robot to follow a sequence of target poses.
    This function demonstrates the capability of controlling the Panda robot using end-effector
    pose sequences with motion planning.
    
    Args:
        env: The robosuite environment
        planner: LiberoMPLibAdapter for motion planning
        target_poses: List of target poses [(pos, quat), ...] where quaternions are in [x,y,z,w] format
        gripper_commands: List of gripper commands corresponding to each pose
        max_steps: Maximum number of steps to run the test
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
    count = 0
    pose_index = 0

    print(f"Starting end-effector pose control with {len(target_poses)} target poses")

    # Run multiple empty actions to ensure the arm is stable
    empty_action = np.zeros(8)
    num_stabilize_steps = 100
    for _ in range(num_stabilize_steps):
        obs, _, _, _ = env.step(empty_action)
        current_joints = planner.get_current_joint_positions(obs)
        current_gripper = planner.get_gripper_joint_positions(obs)
        env.render()

    while pose_index < len(target_poses) and count < max_steps:
        # Get current joint positions from observation
        current_joints = planner.get_current_joint_positions(obs)
        current_gripper = planner.get_gripper_joint_positions(obs)

        # Get target pose
        pos, quat = target_poses[pose_index]
        print(f"Index {pose_index + 1}/{len(target_poses)}: Planning to {pos} {quat}")

        # Plan trajectory to target pose using RRTConnect
        result = planner.plan_to_pose(pos, quat, np.concatenate((current_joints, current_gripper)), use_screw=False)
        if result["status"] != "Success":
            print("Motion planning failed, skipping this pose")
            pose_index += 1
            continue

        # Append several duplicate steps to hold the pose
        duplicate_steps = 10
        last_step = result["position"][-1]
        result["position"] = np.concatenate(
            [result["position"], np.tile(last_step, (duplicate_steps, 1))], axis=0
        )
        
        # Execute the planned trajectory
        n_steps = result["position"].shape[0]
        print(f"Executing trajectory with {n_steps} steps")

        for i in range(n_steps):
            count += 1

            # Get planned joint positions
            planned_joints = result["position"][i]
            current_joints = planner.get_current_joint_positions(obs)
            joint_error = planned_joints - current_joints

            action = np.zeros(8)
            action[:7] = planned_joints - current_joints
            action[7] = gripper_commands[pose_index]  # Set gripper action
            
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
            
        # Calculate pose error after trajectory execution
        # ee_pos = obs["robot0_eef_pos"]
        # ee_quat = obs["robot0_eef_quat"]
        # ee_pos_error = pos - ee_pos
        # ee_quat_error = quat - ee_quat
        # print(f"Pose error - Position: {ee_pos_error}, Quaternion: {ee_quat_error}")
        # print(f"Final EE Pose [{ee_pos[0]:.3f}, {ee_pos[1]:.3f}, {ee_pos[2]:.3f}] [{ee_quat[0]:.3f}, {ee_quat[1]:.3f}, {ee_quat[2]:.3f}, {ee_quat[3]:.3f}]\\n")

        # Move to next pose
        pose_index += 1
        
        # If task completed, break
        if task_completion_hold_count == 0:
            break

    print(f"Total steps: {count}")
    print(f"Completed {pose_index}/{len(target_poses)} poses")
    
    env.close()
    return True


def get_target_poses_for_task(problem_name, language_instruction):
    """
    Define target poses for the robot to track.
    This function provides hardcoded end-effector poses for testing pose-based control.
    
    Note: Quaternions are in [x, y, z, w] format
    
    Returns:
        tuple: (poses, gripper_commands)
            - poses: List of [position, quaternion] pairs where:
                     position = [x, y, z] in meters
                     quaternion = [x, y, z, w] (NOT [w, x, y, z])
            - gripper_commands: List of gripper actions (-1=open, 0=no_change, 1=close)
    """
    # Hardcoded target poses for testing end-effector pose control
    # Format: [[x, y, z], [qx, qy, qz, qw]] - quaternion is in x,y,z,w format
    poses = [
        [[0.0219382, 0.0780828, 1.0067487], [0.9995958, 0.0002424, -0.0284270, -0.0000250]],
        [[0.0240333, 0.0813473, 0.9187534], [0.9995953, 0.0001911, -0.0284460, 0.0001350]],
        [[0.0240333, 0.0813473, 0.9187534], [0.9995953, 0.0001911, -0.0284460, 0.0001350]],
        [[0.0414913, 0.2660626, 0.9825765], [0.9995826, 0.0002256, -0.0288904, -0.0000298]],
        [[0.0414913, 0.2660626, 0.9825765], [0.9995826, 0.0002256, -0.0288904, -0.0000298]],
    ]

    gripper_commands = [
        -1,  # Open gripper
        0,   # No change
        1,   # Close gripper
        1,   # Keep closed
        -1,  # Open gripper
    ]

    print(f"Using {len(poses)} target poses for task: {language_instruction}")
    return poses, gripper_commands


if __name__ == "__main__":
    print("=" * 70)
    print("END-EFFECTOR POSE CONTROL TEST")
    print("=" * 70)
    print("Purpose: Testing the capability of controlling the Panda robot using")
    print("         end-effector pose sequences with motion planning.")
    print("         The robot will follow a sequence of hardcoded target poses")
    print("         (position + orientation) to demonstrate pose-based control.")
    print()
    print("Note: Quaternion format in hardcoded poses is [x, y, z, w]")
    print("=" * 70)
    print()
    
    # Arguments
    parser = argparse.ArgumentParser(description="End-effector pose control using motion planning")
    parser.add_argument(
        "--config",
        type=str,
        default="single-arm-opposed",
        help="Specified environment configuration if necessary",
    )
    parser.add_argument(
        "--camera",
        type=str,
        default="agentview",
        help="Which camera to use for rendering",
    )
    parser.add_argument(
        "--bddl-file",
        type=str,
        default="libero/libero/bddl_files/libero_90/KITCHEN_SCENE1_put_the_black_bowl_on_the_plate.bddl",
        help="Path to the BDDL file for the task"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=5000,
        help="Maximum number of simulation steps"
    )

    args = parser.parse_args()

    # Get controller config
    controller_config = load_controller_config(default_controller="JOINT_POSITION")
    controller_config["kp"] = 150.0
    controller_config["damping_ratio"] = 0.8
    controller_config["output_max"] = 0.5
    controller_config["output_min"] = -0.5
    # print("Controller config:", controller_config)

    # Create argument configuration (hardcoded for Panda)
    config = {
        "robots": ["Panda"],  # Hardcoded to Panda only
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

    # Create motion planner (hardcoded for Panda)
    try:
        planner = LiberoMPLibAdapter(
            urdf_path="./data/panda/panda.urdf",
            srdf_path="./data/panda/panda.srdf",
            move_group="panda_hand"
        )
        print("Motion planner initialized successfully")
    except Exception as e:
        print(f"Failed to initialize motion planner: {e}")
        print("Please check URDF/SRDF paths and ensure mplib is installed")
        exit(1)

    # Load robot base pose for the planner
    base_pose_path = os.path.join("motion_planning", f"{problem_name}/", "base_pose.txt")
    if os.path.exists(base_pose_path):
        with open(base_pose_path, 'r') as f:
            base_pose_data = json.load(f)
        base_pos = np.array(base_pose_data["base_pos"])
        base_quat = np.array(base_pose_data["base_quat"])
        print(f"Loaded robot base pose - Position: {base_pos}, Quaternion: {base_quat}")
        
        # Set the base pose in the planner
        planner.set_base_pose(base_pos, base_quat)
        print("Base pose set successfully in motion planner")
    else:
        print(f"Base pose file not found: {base_pose_path}")
        print("Using default base pose")
        planner.set_base_pose([-0.66, 0.0, 0.912], [0, 0, 0, 1]) 

    # Load gripper-to-hand transform matrix
    if os.path.exists("motion_planning/gripper_to_hand_transform.npy"):
        success = planner.load_and_set_ee_transform("motion_planning/gripper_to_hand_transform.npy")
        if not success:
            print("Failed to load gripper-to-hand transform, using identity matrix")
    else:
        print("No gripper-to-hand transform file found, using identity matrix")

    # Get target poses for this task
    target_poses, gripper_commands = get_target_poses_for_task(problem_name, language_instruction)

    # Run end-effector pose control
    print(f"\\n=== Starting End-Effector Pose Control ===")
    success = end_effector_pose_control(env, planner, target_poses, gripper_commands, args.max_steps)
    
    if success:
        print("✅ End-effector pose control completed successfully")
    else:
        print("❌ End-effector pose control failed")
