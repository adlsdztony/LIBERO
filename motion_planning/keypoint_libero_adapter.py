#!/usr/bin/env python3

import os
import json
import numpy as np
import mplib
from mplib import Pose
import robosuite.utils.transform_utils as transform_utils
from libero_adapter import LiberoMPLibAdapter

# Import GenSim2 KPAM components
import sys
sys.path.append('/home/shaoyu/LIBERO/GenSim2')
from gensim2.env.solver.planner import KPAMPlanner
from gensim2.env.solver.kpam.optimization_problem import OptimizationProblemkPAM
import gensim2.env.solver.kpam.SE3_utils as SE3_utils


class KeypointLiberoMPLibAdapter(LiberoMPLibAdapter):
    """
    Enhanced LIBERO MPLib adapter with keypoint-based motion planning capabilities.
    Integrates GenSim2's KPAM (Keypoint-Augmented Manipulation) solver.
    """

    def __init__(self, urdf_path, srdf_path=None, move_group="panda_hand"):
        """
        Initialize the keypoint-aware planner for LIBERO
        """
        super().__init__(urdf_path, srdf_path, move_group)
        
        # Keypoint management
        self.object_keypoints = {}  # Dict to store loaded keypoints per object
        self.kpam_planner = None    # KPAM planner instance
        
        print("KeypointLiberoMPLibAdapter initialized with KPAM support")

    def load_object_keypoints(self, object_name, keypoints_path):
        """
        Load keypoints for a specific object from JSON file
        
        Args:
            object_name (str): Name of the object (e.g., "microwave", "white_cabinet")
            keypoints_path (str): Path to the keypoints JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(keypoints_path):
                print(f"Warning: Keypoints file not found: {keypoints_path}")
                return False
                
            with open(keypoints_path, 'r') as f:
                keypoints_data = json.load(f)
            
            # Extract keypoints dictionary
            if 'keypoints' in keypoints_data:
                keypoints = keypoints_data['keypoints']
                # Convert to numpy arrays for easier manipulation
                self.object_keypoints[object_name] = {
                    color: np.array(coords) for color, coords in keypoints.items()
                }
                print(f"Loaded {len(keypoints)} keypoints for {object_name}")
                return True
            else:
                print(f"Error: No 'keypoints' field found in {keypoints_path}")
                return False
                
        except Exception as e:
            print(f"Error loading keypoints for {object_name}: {e}")
            return False

    def auto_load_object_keypoints(self, xml_file_path):
        """
        Automatically load keypoints based on XML file path
        
        Args:
            xml_file_path (str): Path to the XML file
            
        Returns:
            bool: True if keypoints were loaded, False otherwise
        """
        # Extract object name from XML path
        xml_dir = os.path.dirname(xml_file_path)
        xml_basename = os.path.splitext(os.path.basename(xml_file_path))[0]
        
        # Try different keypoint file naming patterns
        possible_keypoint_files = [
            os.path.join(xml_dir, f"{xml_basename}_keypoints.json"),
            os.path.join(xml_dir, "keypoints.json"),
        ]
        
        for keypoint_file in possible_keypoint_files:
            if os.path.exists(keypoint_file):
                return self.load_object_keypoints(xml_basename, keypoint_file)
        
        print(f"No keypoints found for {xml_basename}")
        return False

    def get_object_keypoints(self, object_name):
        """
        Get loaded keypoints for an object
        
        Args:
            object_name (str): Name of the object
            
        Returns:
            dict: Dictionary of keypoints {color: np.array([x,y,z])}
        """
        return self.object_keypoints.get(object_name, {})

    def plan_keypoint_to_keypoint(self, object_name, start_keypoint_color, 
                                  target_keypoint_color, current_joint_positions,
                                  use_screw=True):
        """
        Plan motion from one keypoint to another keypoint on the same object
        
        Args:
            object_name (str): Name of the object
            start_keypoint_color (str): Color name of start keypoint (e.g., "red")
            target_keypoint_color (str): Color name of target keypoint (e.g., "blue")  
            current_joint_positions: Current joint angles (7 elements)
            use_screw: Try screw motion first, fallback to RRT if needed
            
        Returns:
            dict: Planning result with 'status', 'position', etc.
        """
        if object_name not in self.object_keypoints:
            return {"status": "Failed", "error": f"No keypoints loaded for {object_name}"}
        
        keypoints = self.object_keypoints[object_name]
        
        if start_keypoint_color not in keypoints:
            return {"status": "Failed", "error": f"Start keypoint '{start_keypoint_color}' not found"}
        
        if target_keypoint_color not in keypoints:
            return {"status": "Failed", "error": f"Target keypoint '{target_keypoint_color}' not found"}
        
        # Get target keypoint position
        target_pos = keypoints[target_keypoint_color]
        
        # For now, use current orientation (could be enhanced with keypoint-based orientation)
        current_pose = self.get_fk_ee_pose(current_joint_positions)
        target_quat = current_pose.q  # Keep current orientation
        
        # Convert mplib quaternion format to libero format [qx, qy, qz, qw]
        w, x, y, z = target_quat  
        libero_quat = [x, y, z, w]
        
        print(f"Planning motion from {start_keypoint_color} to {target_keypoint_color} keypoint")
        print(f"Target position: {target_pos}")
        
        # Use existing pose planning with keypoint target
        return self.plan_to_pose(target_pos, libero_quat, current_joint_positions, use_screw)

    def plan_to_keypoint(self, object_name, keypoint_color, current_joint_positions, 
                         use_screw=True):
        """
        Plan motion to a specific keypoint on an object
        
        Args:
            object_name (str): Name of the object
            keypoint_color (str): Color name of target keypoint (e.g., "red")
            current_joint_positions: Current joint angles (7 elements)
            use_screw: Try screw motion first, fallback to RRT if needed
            
        Returns:
            dict: Planning result with 'status', 'position', etc.
        """
        if object_name not in self.object_keypoints:
            return {"status": "Failed", "error": f"No keypoints loaded for {object_name}"}
        
        keypoints = self.object_keypoints[object_name]
        
        if keypoint_color not in keypoints:
            return {"status": "Failed", "error": f"Keypoint '{keypoint_color}' not found"}
        
        # Get target keypoint position
        target_pos = keypoints[keypoint_color]
        
        # Use current orientation (could be enhanced with keypoint-based orientation)
        current_pose = self.get_fk_ee_pose(current_joint_positions)
        target_quat = current_pose.q
        
        # Convert mplib quaternion format to libero format [qx, qy, qz, qw]
        w, x, y, z = target_quat
        libero_quat = [x, y, z, w]
        
        print(f"Planning motion to {keypoint_color} keypoint on {object_name}")
        print(f"Target position: {target_pos}")
        
        return self.plan_to_pose(target_pos, libero_quat, current_joint_positions, use_screw)

    def plan_with_kpam_constraints(self, object_name, keypoint_constraints,
                                   current_joint_positions, use_screw=True):
        """
        Plan motion using KPAM solver with keypoint constraints
        
        Args:
            object_name (str): Name of the object
            keypoint_constraints (list): List of keypoint constraint dicts
                Each dict should have: {"keypoint": "red", "target_pos": [x,y,z]}
            current_joint_positions: Current joint angles (7 elements)
            use_screw: Try screw motion first, fallback to RRT if needed
            
        Returns:
            dict: Planning result with 'status', 'position', etc.
        """
        if object_name not in self.object_keypoints:
            return {"status": "Failed", "error": f"No keypoints loaded for {object_name}"}
        
        # TODO: Implement full KPAM optimization here
        # For now, use the first keypoint constraint as target
        if len(keypoint_constraints) > 0:
            first_constraint = keypoint_constraints[0]
            target_pos = np.array(first_constraint["target_pos"])
            
            # Use current orientation
            current_pose = self.get_fk_ee_pose(current_joint_positions)
            target_quat = current_pose.q
            
            # Convert mplib quaternion format to libero format
            w, x, y, z = target_quat
            libero_quat = [x, y, z, w]
            
            print(f"Planning with KPAM constraints for {object_name}")
            print(f"Target position: {target_pos}")
            
            return self.plan_to_pose(target_pos, libero_quat, current_joint_positions, use_screw)
        
        return {"status": "Failed", "error": "No keypoint constraints provided"}

    def list_object_keypoints(self, object_name):
        """
        List all available keypoints for an object
        
        Args:
            object_name (str): Name of the object
            
        Returns:
            dict: Dictionary of keypoints or empty dict if not found
        """
        keypoints = self.get_object_keypoints(object_name)
        if keypoints:
            print(f"Available keypoints for {object_name}:")
            for color, pos in keypoints.items():
                print(f"  {color}: [{pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f}]")
        else:
            print(f"No keypoints loaded for {object_name}")
        return keypoints

    def get_loaded_objects(self):
        """
        Get list of objects with loaded keypoints
        
        Returns:
            list: List of object names with keypoints
        """
        return list(self.object_keypoints.keys())