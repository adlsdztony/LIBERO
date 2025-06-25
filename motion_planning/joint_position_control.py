#!/usr/bin/env python3

import argparse
import json
import numpy as np
import os
import time

import libero.libero.envs.bddl_utils as BDDLUtils
from libero.libero.envs import *
from robosuite import load_controller_config
from robosuite.wrappers import VisualizationWrapper


def collect_joint_position_trajectory(env, target_joint_positions, max_steps=1000):
    """
    Test joint position control by commanding the robot to track fixed joint positions.
    This function demonstrates the capability of the robosuite JOINT_POSITION controller
    to control individual joint positions of the Panda robotic arm.
    
    Args:
        env: The robosuite environment
        target_joint_positions: Target joint positions to track (7 values for Panda arm)
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
    saving = True
    count = 0

    print(f"Starting joint position control")
    print(f"Target joint positions: {[f'{j:.3f}' for j in target_joint_positions]}")

    # Get initial observation with empty action
    empty_action = np.zeros(8)
    obs, _, _, _ = env.step(empty_action)
    
    while count < max_steps:
        count += 1

        # Get current joint positions from observation
        current_joints = obs['robot0_joint_pos']
        
        # Calculate joint position error
        joint_error = np.array(target_joint_positions) - np.array(current_joints)
        
        # Create action (joint position control)
        action = np.zeros(8)
        action[:7] = joint_error  # Position error as action
        
        if count % 100 == 0:
            print(f"Step {count}:")
            print(f"  Current joints: {current_joints.tolist()}")
            print(f"  Target joints:  {target_joint_positions.tolist()}")
            print(f"  Joint error:    {joint_error.tolist()}")
            print(f"  Max error:      {np.max(np.abs(joint_error)):.3f}")
        
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

    print(f"Total steps: {count}")
    env.close()
    return saving


def get_target_joint_positions():
    """
    Define the target joint positions for the robot to track.
    This is a hardcoded joint configuration for testing purposes.
    
    Returns:
        np.ndarray: Target joint positions (7 values for Panda arm joints)
    """
    # Hardcoded target joint positions for testing joint position control
    # These values represent a specific pose of the Panda arm
    target_joints = np.array([-0.006, 0.358, -0.010, -1.705, 0.003, 2.006, 0.768])

    print(f"Using hardcoded target joint positions: {[f'{j:.3f}' for j in target_joints]}")
    return target_joints


if __name__ == "__main__":
    print("=" * 60)
    print("JOINT POSITION CONTROL TEST")
    print("=" * 60)
    print("Purpose: Testing the capability of the robosuite JOINT_POSITION controller")
    print("         to control the joint positions of the Panda robotic arm.")
    print("         The robot will move to a predefined hardcoded joint configuration.")
    print("=" * 60)
    print()
    
    # Arguments
    parser = argparse.ArgumentParser(description="Test joint position control for Panda robot")
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
        help="Path to the BDDL file defining the task",
    )
    args = parser.parse_args()

    # Get controller config
    controller_config = load_controller_config(default_controller="JOINT_POSITION")
    controller_config["kp"] = 150.0
    controller_config["damping_ratio"] = 0.8
    controller_config["output_max"] = 0.8
    controller_config["output_min"] = -0.8

    config = {
        "robots": ["Panda"],
        "controller_configs": controller_config,
    }

    assert os.path.exists(args.bddl_file)
    problem_info = BDDLUtils.get_problem_info(args.bddl_file)
    
    # Create environment
    problem_name = problem_info["problem_name"]
    language_instruction = problem_info["language_instruction"]
    
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

    # Get target joint positions
    target_joint_positions = get_target_joint_positions()

    # Run joint position control (no data collection needed for testing)
    print(f"\n=== Starting Joint Position Control ===")
    collect_joint_position_trajectory(env, target_joint_positions, max_steps=2000)
