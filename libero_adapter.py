#!/usr/bin/env python3

import numpy as np
import mplib
from mplib import Pose


class LiberoMPLibAdapter:
    """
    Adapter class to use MPlib planner in LIBERO environment.
    This removes all Sapien dependencies and provides LIBERO-specific interfaces.
    """

    def __init__(self, urdf_path, srdf_path=None, move_group="panda_hand"):
        """
        Initialize the planner for LIBERO
        
        Args:
            urdf_path: Path to robot URDF file
            srdf_path: Path to robot SRDF file (optional)
            move_group: Name of the move group (end effector)
        """
        # Setup the standalone motion planner (no simulation dependencies)
        self.planner = mplib.Planner(
            urdf=urdf_path,
            srdf=srdf_path,
            move_group=move_group,
        )
        
        # Store move group info for joint mapping
        self.move_group_joint_indices = self.planner.move_group_joint_indices
        
    def plan_to_pose(self, target_pose, current_joint_positions, use_screw=True):
        """
        Plan a path to target pose
        
        Args:
            target_pose: [x, y, z, qx, qy, qz, qw] - position and quaternion
            current_joint_positions: Current joint angles for move group
            use_screw: Try screw motion first, fallback to RRT if needed
            
        Returns:
            dict: Planning result with 'status', 'position', 'velocity', etc.
        """
        # Convert target pose to mplib.Pose
        if isinstance(target_pose, (list, np.ndarray)):
            pose = Pose(target_pose[:3], target_pose[3:])
        else:
            pose = target_pose
            
        if use_screw:
            # Try screw motion first (straight line interpolation)
            result = self.planner.plan_screw(
                pose, current_joint_positions, time_step=1/250
            )
            if result["status"] == "Success":
                return result
                
        # Fallback to sampling-based planning (RRTConnect)
        result = self.planner.plan_pose(
            pose, current_joint_positions, time_step=1/250
        )
        return result
    
    def plan_to_joint_positions(self, target_joints, current_joint_positions):
        """
        Plan a path to target joint configuration
        
        Args:
            target_joints: Target joint angles for move group
            current_joint_positions: Current joint angles for move group
            
        Returns:
            dict: Planning result
        """
        result = self.planner.plan_qpos(
            target_joints, current_joint_positions, time_step=1/250
        )
        return result
    
    def execute_path_in_libero(self, libero_env, result, arm_action_type="joint_position"):
        """
        Execute planned path in LIBERO environment
        
        Args:
            libero_env: LIBERO environment instance
            result: Planning result from plan_to_pose() or plan_to_joint_positions()
            arm_action_type: "joint_position" or "joint_velocity"
            
        Returns:
            bool: True if execution successful
        """
        if result["status"] != "Success":
            print(f"Planning failed: {result['status']}")
            return False
            
        n_steps = result["position"].shape[0]
        
        for i in range(n_steps):
            if arm_action_type == "joint_position":
                # Set joint positions directly
                arm_action = result["position"][i]
            elif arm_action_type == "joint_velocity":
                # Use joint velocities 
                arm_action = result["velocity"][i]
            else:
                raise ValueError(f"Unsupported arm_action_type: {arm_action_type}")
                
            # Create LIBERO action (this depends on LIBERO's action space)
            # Typically: [arm_joints (7), gripper (1 or 2)]
            action = np.zeros(libero_env.action_space.shape[0])
            
            # Fill in arm joint actions (first 7 DOF for Panda)
            action[:len(self.move_group_joint_indices)] = arm_action
            
            # Keep gripper unchanged (or add gripper control logic)
            # action[-1] = gripper_action  # if needed
            
            # Step the environment
            obs, reward, done, info = libero_env.step(action)
            
            if done:
                break
                
        return True
    
    def get_current_pose(self, libero_env):
        """
        Get current end-effector pose from LIBERO environment
        
        Args:
            libero_env: LIBERO environment instance
            
        Returns:
            Pose: Current end-effector pose
        """
        # Get current joint positions from LIBERO
        current_qpos = self.get_current_joint_positions(libero_env)
        
        # Use forward kinematics to get end-effector pose
        ee_pose = self.planner.robot.get_pinocchio_model().compute_forward_kinematics(
            current_qpos
        )
        
        return ee_pose
    
    def get_current_joint_positions(self, libero_env):
        """
        Extract current joint positions from LIBERO observation
        
        Args:
            libero_env: LIBERO environment instance
            
        Returns:
            np.ndarray: Current joint positions for move group
        """
        # This depends on LIBERO's observation structure
        # Typically obs contains robot joint states
        obs = libero_env._get_obs()
        
        # Extract joint positions (this may need adjustment based on LIBERO version)
        if hasattr(obs, 'robot0_joint_pos'):
            joint_pos = obs['robot0_joint_pos']
        elif 'robot0_joint_pos' in obs:
            joint_pos = obs['robot0_joint_pos']
        else:
            # Fallback: try to get from robot directly
            joint_pos = libero_env.robots[0].sim.data.qpos[
                libero_env.robots[0]._ref_joint_pos_indexes
            ]
            
        # Return only move group joints
        return joint_pos[self.move_group_joint_indices]
    
    def update_collision_objects(self, objects):
        """
        Update collision environment with objects from LIBERO scene
        
        Args:
            objects: List of collision objects or point clouds
        """
        # Clear existing objects
        self.planner.planning_world.clear_objects()
        
        # Add new objects
        for obj in objects:
            if hasattr(obj, 'point_cloud'):
                # Add as point cloud
                self.planner.update_point_cloud(obj.point_cloud, resolution=0.01)
            elif hasattr(obj, 'mesh'):
                # Add as mesh object
                self.planner.planning_world.add_object(obj)
    
    def check_collision(self, joint_positions=None):
        """
        Check for collisions at given joint configuration
        
        Args:
            joint_positions: Joint positions to check (None for current)
            
        Returns:
            bool: True if collision detected
        """
        # Check self-collision
        self_collisions = self.planner.check_for_self_collision(joint_positions)
        
        # Check environment collision  
        env_collisions = self.planner.check_for_env_collision(joint_positions)
        
        return len(self_collisions) > 0 or len(env_collisions) > 0
    
    def solve_ik(self, target_pose, seed_qpos=None):
        """
        Solve inverse kinematics for target pose
        
        Args:
            target_pose: Target end-effector pose [x,y,z,qx,qy,qz,qw]
            seed_qpos: Seed joint configuration
            
        Returns:
            tuple: (status, joint_positions)
        """
        if isinstance(target_pose, (list, np.ndarray)):
            pose = Pose(target_pose[:3], target_pose[3:])
        else:
            pose = target_pose
            
        if seed_qpos is None:
            seed_qpos = np.zeros(len(self.move_group_joint_indices))
            
        status, result = self.planner.IK(pose, seed_qpos)
        
        if status == "Success":
            return status, result[0]  # Return first solution
        else:
            return status, None


# Example usage function
def create_libero_planner(robot_type="panda"):
    """
    Factory function to create planner for different robot types in LIBERO
    
    Args:
        robot_type: Type of robot ("panda", "ur5", etc.)
        
    Returns:
        LiberoMPLibAdapter: Configured planner
    """
    if robot_type.lower() == "panda":
        return LiberoMPLibAdapter(
            urdf_path="./data/panda/panda.urdf",
            srdf_path="./data/panda/panda.srdf", 
            move_group="panda_hand"
        )
    else:
        raise NotImplementedError(f"Robot type {robot_type} not supported yet")


# Example integration with LIBERO
def example_libero_integration():
    """
    Example showing how to integrate MPlib with LIBERO
    """
    import libero  # Assuming LIBERO is installed
    
    # Create LIBERO environment
    env = libero.make("your_task_name")
    
    # Create motion planner
    planner = create_libero_planner("panda")
    
    # Reset environment
    obs = env.reset()
    
    # Plan to a target pose
    target_pose = [0.5, 0.0, 0.3, 0, 1, 0, 0]  # [x,y,z,qx,qy,qz,qw]
    current_joints = planner.get_current_joint_positions(env)
    
    # Plan path
    result = planner.plan_to_pose(target_pose, current_joints)
    
    # Execute path
    success = planner.execute_path_in_libero(env, result)
    
    print(f"Motion execution {'succeeded' if success else 'failed'}")
    
    env.close()


if __name__ == "__main__":
    # Run example
    example_libero_integration()
