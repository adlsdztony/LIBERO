#!/usr/bin/env python3

import numpy as np
import mplib
from mplib import Pose


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
    
    def libero_to_mplib_quaternion(self, libero_quat):
        x, y, z, w = libero_quat
        mplib_quat = [w, x, y, z]
        return mplib_quat

    def set_base_pose(self, base_pose):
        pass

    def get_current_joint_positions(self, obs):
        """
        Extract current joint positions from LIBERO observation
        
        Args:
            obs: Observation dict from env.step() or env.reset()
            
        Returns:
            np.ndarray: Current joint positions (7 elements for Panda)
        """
        return obs['robot0_joint_pos']
    
    def get_fk_ee_pose(self, joint_positions):
        """
        Get end-effector pose from joint positions using MPLib FK
        
        Args:
            joint_positions: Joint angles (7 elements)
            
        Returns:
            Pose: End-effector pose as mplib.Pose object
        """
        pose = self.planner.get_fk(joint_positions)
        return pose
        
    def plan_to_pose(self, pos, quat, current_joint_positions, use_screw=True):
        """
        Plan a path to target pose
        
        Args:
            pos: x, y, z
            quat: libero eef quat
            current_joint_positions: Current joint angles (7 elements)
            use_screw: Try screw motion first, fallback to RRT if needed
            
        Returns:
            dict: Planning result with 'status', 'position', etc.
        """
        # Convert target pose to mplib.Pose
        mplib_quat = self.libero_to_mplib_quaternion(quat)
        pose = Pose(pos, mplib_quat)

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


# Example usage function
def create_libero_planner(urdf_path="./data/panda/panda.urdf", srdf_path="./data/panda/panda.srdf"):
    """
    Create planner for Panda robot
    """
    return LiberoMPLibAdapter(
        urdf_path=urdf_path,
        srdf_path=srdf_path, 
        move_group="panda_hand"
    )
