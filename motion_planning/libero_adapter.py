#!/usr/bin/env python3

import numpy as np
import mplib
from mplib import Pose
import robosuite.utils.transform_utils as transform_utils


class LiberoMPLibAdapter:
    """
    Simple adapter class to use MPlib planner in LIBERO environment. 
    LIBERO obs.eef_quat is in [qx, qy, qz, qw] format
    """

    def __init__(self, urdf_path, srdf_path=None, move_group="panda_hand"):
        """
        Initialize the planner for LIBERO
        """
        self.planner = mplib.Planner(
            urdf=urdf_path,
            srdf=srdf_path,
            move_group=move_group,
            joint_vel_limits=np.full(7, 0.3),
        )
        self.ee2move_group = np.eye(4)
        self.move_group2ee = np.eye(4)
    
    def libero_to_mplib_quaternion(self, libero_quat):
        x, y, z, w = libero_quat
        mplib_quat = [w, x, y, z]
        return mplib_quat
    
    def set_ee_transform(self, ee_tf:np.ndarray):
        """
        Set the transform from eef to the move group for the planner
        e.g. the transform from the Panda's "gripper" to the "hand" (move group)
        
        Args:
            ee_tf: End-effector transform as a 4x4 numpy array
        """
        self.ee2move_group = ee_tf
        self.move_group2ee = np.linalg.inv(ee_tf)

    def set_base_pose(self, base_pos, base_quat):
        """
        Set the base pose for the planner
        
        Args:
            base_pos: Base position as [x, y, z]
            base_quat: Base orientation as [qx, qy, qz, qw]
        """
        mplib_quat = self.libero_to_mplib_quaternion(base_quat)
        base_pose = Pose(base_pos, mplib_quat)
        self.planner.set_base_pose(base_pose)

    def load_and_set_ee_transform(self, npy_file_path):
        """
        Load gripper-to-hand transform matrix from npy file and set it in the planner
        
        Args:
            npy_file_path: Path to the .npy file containing the 4x4 transform matrix
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load the transform matrix from npy file
            gripper_to_hand_transform = np.load(npy_file_path)
            
            # Validate matrix shape
            if gripper_to_hand_transform.shape != (4, 4):
                print(f"Error: Expected 4x4 matrix, got {gripper_to_hand_transform.shape}")
                return False
            
            print(f"Loaded gripper-to-hand transform from {npy_file_path}:")
            # print(gripper_to_hand_transform)
            
            # Set the transform in the planner
            self.set_ee_transform(gripper_to_hand_transform)
            print("Gripper-to-hand transform set successfully in motion planner")
            return True
            
        except FileNotFoundError:
            print(f"Error: Transform file not found: {npy_file_path}")
            return False
        except Exception as e:
            print(f"Error loading gripper-to-hand transform: {e}")
            return False


    def get_current_joint_positions(self, obs):
        """
        Extract current joint positions from LIBERO observation
        
        Args:
            obs: Observation dict from env.step() or env.reset()
            
        Returns:
            np.ndarray: Current joint positions (7 elements for Panda)
        """
        return obs['robot0_joint_pos']

    def get_gripper_joint_positions(self, obs):
        """
        Extract gripper joint positions from LIBERO observation
        
        Args:
            obs: Observation dict from env.step() or env.reset()
            
        Returns:
            np.ndarray: Gripper joint positions (2 elements for Panda)
        """
        return obs['robot0_gripper_qpos']
    
    def get_fk_ee_pose(self, joint_positions):
        """
        Get end-effector pose from joint positions using MPLib FK
        
        Args:
            joint_positions: Joint angles (7 elements)
            
        Returns:
            Pose: End-effector pose as mplib.Pose object
        """
        pose = self.planner.get_current_end_effector_pose(joint_positions)
        return pose
        
    def plan_to_pose(self, pos, quat, current_joint_positions, use_screw=True):
        """
        Plan a path to target pose. Input ee pose will be transformed to the move group frame.
        
        Args:
            pos: x, y, z
            quat: libero eef quat
            current_joint_positions: Current joint angles (7 elements)
            use_screw: Try screw motion first, fallback to RRT if needed
            
        Returns:
            dict: Planning result with 'status', 'position', etc.
        """
        # Get target move group pose
        ee2world = np.eye(4)
        ee2world[:3, 3] = pos
        ee2world[:3, :3] = transform_utils.quat2mat(quat)
        move_group2world = ee2world @ self.move_group2ee
        # Convert target pose to mplib.Pose
        x, y, z, w = transform_utils.mat2quat(move_group2world[:3, :3])
        pose = Pose(
            move_group2world[:3, 3],
            [w, x, y, z]
        )
        if use_screw:
            # Try screw motion first (straight line interpolation)
            result = self.planner.plan_screw(
                pose, current_joint_positions, time_step=1/20
            )
            if result["status"] == "Success":
                return result
                
        # Fallback to sampling-based planning (RRTConnect)
        result = self.planner.plan_pose(
            pose, current_joint_positions, time_step=1/20
        )
        return result
