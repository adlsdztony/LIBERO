"""
Dynamic Scene Creation for LIBERO MU Generation

This file dynamically creates scene classes from JSON data, replacing the original
hardcoded scene definitions in mu_creation.py.

The JSON data contains scene configurations with:
- fixture_num_info and object_num_info for scene setup
- regions with coordinates, names, and rotation data
- init_states for object placement

This approach allows for easier maintenance and configuration of scenes.
"""

import json
import math
import numpy as np
from pathlib import Path
from libero.libero.envs import objects
from libero.libero.utils.bddl_generation_utils import *
from libero.libero.envs.objects import OBJECTS_DICT
from libero.libero.utils.object_utils import get_affordance_regions
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates

# Constants
KITCHEN_TABLE_HEIGHT = 0.875
LIVING_ROOM_TABLE_HEIGHT = 0.41
STUDY_TABLE_HEIGHT = 0.67
TABLE_HEIGHT = 0.895


def convert_yaw_rotation_to_numpy(yaw_rotation):
    """
    Convert float yaw_rotation values back to numpy expressions.
    
    Args:
        yaw_rotation: List of [min, max] float values representing multiples of pi
        
    Returns:
        Tuple of numpy expressions equivalent to the original code
    """
    if yaw_rotation == [0.0, 0.0]:
        return (0.0, 0.0)
    elif yaw_rotation == [1.0, 1.0]:
        return (np.pi, np.pi)
    elif yaw_rotation == [-0.5, -0.25]:
        return (-np.pi/2, -np.pi/4)
    elif yaw_rotation == [0, 0]:
        return (0, 0)
    else:
        # Convert back to numpy expressions
        min_val, max_val = yaw_rotation
        min_expr = min_val * np.pi if min_val != 0 else 0.0
        max_expr = max_val * np.pi if max_val != 0 else 0.0
        return (min_expr, max_expr)


def get_table_name_for_scene_type(scene_type):
    """
    Get the appropriate table name based on scene type.
    
    Args:
        scene_type: The scene type identifier
        
    Returns:
        Table name to use for the given scene type
    """
    table_mapping = {
        "kitchen": "kitchen_table",
        "living_room": "living_room_table", 
        "study": "study_table",
        "tabletop_manipulation": "main_table",
        "coffee": "coffee_table",
    }
    return table_mapping.get(scene_type, "table")


def substitute_scene_table_placeholder(data, scene_type):
    """
    Replace {scene_table} placeholder with appropriate table name.
    
    Args:
        data: Dictionary that may contain {scene_table} placeholder
        scene_type: Scene type to determine table name
        
    Returns:
        Dictionary with placeholders replaced
    """
    table_name = get_table_name_for_scene_type(scene_type)
    
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            new_key = key.replace("{scene_table}", table_name)
            result[new_key] = substitute_scene_table_placeholder(value, scene_type)
        return result
    elif isinstance(data, list):
        return [substitute_scene_table_placeholder(item, scene_type) for item in data]
    elif isinstance(data, str):
        return data.replace("{scene_table}", table_name)
    else:
        return data


def create_scene_class(scene_data, scene_type):
    """
    Dynamically create a scene class from JSON data.
    
    Args:
        scene_data: Dictionary containing scene configuration
        scene_type: The scene type for this class
        
    Returns:
        Dynamically created scene class
    """
    scene_name = scene_data["name"]    # Generate class name based on scene type and scene number
    scene_number = scene_name.replace("Scene", "")
    class_name = f"{scene_type}_{scene_name.lower()}"
    if scene_type == "tabletop_manipulation":
        class_name = f"tabletop_scene{scene_number}"
    
    # Substitute placeholders with actual table names

    if scene_type == "tabletop_manipulation":
        fixture_num_info = substitute_scene_table_placeholder(scene_data["fixture_num_info"], "table")
    else:
        fixture_num_info = substitute_scene_table_placeholder(scene_data["fixture_num_info"], scene_type)
    object_num_info = substitute_scene_table_placeholder(scene_data["object_num_info"], scene_type)
    regions = substitute_scene_table_placeholder(scene_data["regions"], scene_type)
    init_states = substitute_scene_table_placeholder(scene_data["init_states"], scene_type)
    
    # Get workspace name
    table_name = get_table_name_for_scene_type(scene_type)
    
    class DynamicSceneClass(InitialSceneTemplates):
        def __init__(self):
            super().__init__(
                workspace_name=table_name,
                fixture_num_info=fixture_num_info,
                object_num_info=object_num_info,
            )

        def define_regions(self):
            self.regions.update(
                self.get_region_dict(
                        region_centroid_xy=[0.0, 0.0],
                        region_name="table_region",
                        target_name=self.workspace_name,
                        region_half_len=100,
                        yaw_rotation=(0.0, 0.0),
                )
            )
            for region in regions:
                yaw_rotation = convert_yaw_rotation_to_numpy(region["yaw_rotation"])
                
                self.regions.update(
                    self.get_region_dict(
                        region_centroid_xy=region["region_centroid_xy"],
                        region_name=region["region_name"],
                        target_name=self.workspace_name,
                        region_half_len=region["region_half_len"],
                        yaw_rotation=yaw_rotation,
                    )
                )
            
            self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
                self.regions
            )

        @property
        def init_states(self):
            return [tuple(state) for state in init_states]
    
    # Set class name for proper registration
    DynamicSceneClass.__name__ = class_name
    DynamicSceneClass.__qualname__ = class_name
    
    return DynamicSceneClass


def load_and_register_scenes():
    """
    Load scenes from individual JSON files and register them dynamically.
    Generate all combinations of scene types and scenes (21 scenes × 4 types = 84 classes).
    """
    # Get the path to the scenes directory
    current_dir = Path(__file__).parent
    scenes_dir = current_dir / "scenes"
    
    if not scenes_dir.exists():
        print(f"Warning: Could not find scenes directory at {scenes_dir}")
        return
    
    # Load all scene files
    scene_files = sorted(scenes_dir.glob("Scene*.json"))
    if not scene_files:
        print(f"Warning: No scene files found in {scenes_dir}")
        return
    
    print(f"Loading {len(scene_files)} scene files from {scenes_dir}")
    
    # Define all scene types
    scene_types = ["kitchen", "living_room", "study", "tabletop_manipulation", "coffee"]
    
    # Create and register scene classes for all combinations
    for scene_file in scene_files:
        try:
            with open(scene_file, 'r') as f:
                scene_data = json.load(f)
            
            # print(f"Loaded scene data from {scene_file.name}")
            
            # Generate classes for all scene types
            for scene_type in scene_types:
                scene_class = create_scene_class(scene_data, scene_type)
                
                # Register the scene class
                registered_class = register_mu(scene_type=scene_type)(scene_class)
                
                # Add to global namespace for compatibility
                globals()[scene_class.__name__] = registered_class
                
                # print(f"  ✓ Registered {scene_class.__name__} for {scene_type}")
                
        except Exception as e:
            print(f"Error loading scene file {scene_file.name}: {e}")
            continue


# Load and register all scenes when this module is imported
load_and_register_scenes()
