"""
Utility functions for robot pose analysis and logging.
"""

import numpy as np
import os
import json
from datetime import datetime
import robosuite.utils.transform_utils as transform_utils



def get_robot_base_pose(robot, obs):
    """
    Get robot base pose (position and orientation).
    
    Args:
        robot: Active robot object from the simulation
        obs: Observation dictionary from environment step
    
    Returns:
        tuple: (base_position, base_orientation)
    """
    base_pos = robot.base_pos
    base_ori = robot.base_ori
    return base_pos, base_ori


def get_gripper_hand_pose_in_base(robot, obs):
    """
    Get gripper and hand poses in base frame, plus hand-to-gripper transform.
    
    Args:
        robot: Active robot object from the simulation
        obs: Observation dictionary from environment step
    
    Returns:
        tuple: (gripper_pose, hand_pose, gripper_to_hand_transform, hand_to_gripper_transform)
    """
    eef_pos, eef_quat = get_eef_pose_in_world(robot, obs)
    eef2world_tf = np.eye(4)
    eef2world_tf[:3, 3] = eef_pos
    eef2world_tf[:3, :3] = transform_utils.quat2mat(eef_quat)
    
    base2world_tf = np.eye(4)
    base2world_tf[:3, 3] = robot.base_pos
    base2world_tf[:3, :3] = transform_utils.quat2mat(robot.base_ori)

    gripper_pose = np.linalg.inv(base2world_tf) @ eef2world_tf
    
    right_hand_pose = robot.pose_in_base_from_name("robot0_right_hand")
    gripper_to_hand = np.linalg.inv(right_hand_pose) @ gripper_pose
    hand_to_gripper = np.linalg.inv(gripper_pose) @ right_hand_pose
    return gripper_pose, right_hand_pose, gripper_to_hand, hand_to_gripper


def get_eef_pose_in_world(robot, obs):
    """
    Get end effector pose in world coordinates.
    
    Args:
        robot: Active robot object from the simulation
        obs: Observation dictionary from environment step
    
    Returns:
        tuple: (eef_position, eef_quaternion)
    """
    eef_pos = obs['robot0_eef_pos']
    eef_quat = obs['robot0_eef_quat']
    return eef_pos, eef_quat


def get_joint_positions(robot, obs):
    """
    Get current joint positions.
    
    Args:
        robot: Active robot object from the simulation
        obs: Observation dictionary from environment step
    
    Returns:
        np.ndarray: Joint positions
    """
    return obs["robot0_joint_pos"]


def print_robot_pose_info(robot, obs):
    """
    Print detailed robot pose information using the getter functions.
    
    Args:
        robot: Active robot object from the simulation
        obs: Observation dictionary from environment step
    
    Returns:
        dict: Dictionary containing pose information
    """
        
    pose_info = {}
    
    try:
        # Get robot base pose
        base_pos, base_ori = get_robot_base_pose(robot, obs)
        pose_info['base_pos'] = base_pos.tolist() if hasattr(base_pos, 'tolist') else base_pos
        pose_info['base_ori'] = base_ori.tolist() if hasattr(base_ori, 'tolist') else base_ori
        print(f"🤖 Robot base pose - Position: {base_pos}, Orientation: {base_ori}")
        
        # Get gripper and hand poses
        gripper_pose, right_hand_pose, gripper_to_hand, hand_to_gripper = get_gripper_hand_pose_in_base(robot, obs)
        pose_info['gripper_pose'] = gripper_pose.tolist()
        pose_info['right_hand_pose'] = right_hand_pose.tolist()
        pose_info['gripper_to_hand'] = hand_to_gripper.tolist()
        print(f"🤖 Gripper pose in base:\n{gripper_pose}")
        print(f"🤖 Right hand pose in base:\n{right_hand_pose}")
        print(f"🤖 gripper to hand transform:\n{gripper_to_hand}")

        # End effector in world coordinates
        eef_pos, eef_quat = get_eef_pose_in_world(robot, obs)
        pose_info['eef_pos'] = eef_pos.tolist()
        pose_info['eef_quat'] = eef_quat.tolist()
        print(f"🤖 End effector pose in world: pos {eef_pos}, quat {eef_quat}")

        eef2world_tf = np.eye(4)
        eef2world_tf[:3, 3] = eef_pos
        eef2world_tf[:3, :3] = transform_utils.quat2mat(eef_quat)
        pose_info['eef2world_tf'] = eef2world_tf.tolist()  # Convert to list for JSON serialization
        print(f"🤖 End effector transform in world coordinates:\n{eef2world_tf}")

        # Joint positions
        joint_pos = get_joint_positions(robot, obs)
        pose_info['joint_positions'] = joint_pos.tolist()
        print(f"🤖 Joint positions: {joint_pos}")
        
    except Exception as e:
        print(f"🤖 Error extracting pose information: {e}")
        pose_info['error'] = str(e)
    
    return pose_info


def save_transform_matrix(transform_matrix, filename=None):
    """
    Save a 4x4 transformation matrix to current directory.
    
    Args:
        transform_matrix (np.ndarray): 4x4 transformation matrix
        filename (str, optional): Custom filename. If None, a timestamped filename will be created.
    
    Returns:
        str: Filename of saved file
    """
    # Ensure the matrix is 4x4
    if not isinstance(transform_matrix, np.ndarray) or transform_matrix.shape != (4, 4):
        raise ValueError("Transform matrix must be a 4x4 numpy array")
    # Create timestamped filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
        filename = f"transform_matrix_{timestamp}.npy"
    # Save as numpy file in current directory
    np.save(filename, transform_matrix)
    
    print(f"✅ Transform matrix saved to {filename}")
    return filename


def load_transform_matrix(filename):
    """
    Load a transformation matrix from file.
    
    Args:
        filename (str): Path to the .npy file
        
    Returns:
        np.ndarray: Loaded transformation matrix
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Transform matrix file {filename} not found")
    
    transform_matrix = np.load(filename)
    return transform_matrix


def save_gripper_to_hand_transform(robot, obs):
    """
    Extract and save the gripper to hand transformation matrix.
    
    Args:
        robot: Active robot object
        obs: Observation dictionary from environment step
        
    Returns:
        tuple: (gripper_to_hand_transform, filename)
    """
    try:
        # Get gripper and hand poses using the getter function
        _, _, gripper_to_hand, _ = get_gripper_hand_pose_in_base(robot, obs)
        
        # Get the directory of the current file (pose_utils.py)
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create the full path for the transform file
        filename = os.path.join(current_file_dir, "gripper_to_hand_transform.npy")
        
        # Save the transform using the full path
        np.save(filename, gripper_to_hand)
        
        print(f"✅ Gripper-to-hand transform saved to {filename}")
        return gripper_to_hand, filename
        
    except Exception as e:
        print(f"❌ Error saving gripper to hand transform: {e}")
        return None, None
