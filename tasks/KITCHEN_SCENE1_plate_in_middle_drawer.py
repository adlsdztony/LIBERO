# Put the bowl in the middle drawer, slightly tilt it toward the front edge, and close the drawer halfway.
"""This is a standalone file for create a task in libero."""
import numpy as np

from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    get_task_info,
    generate_bddl_from_task_info,
)

from libero.libero.benchmark.mu_creation import *

def main():
    scene_name = "kitchen_scene1"
    language = "Put the plate in the middle drawer and close the drawer"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_cabinet_1", "plate_1"],
            goal_states = [
            ("In", "plate_1", "wooden_cabinet_1_middle_region"),
            ("Close", "wooden_cabinet_1_middle_region"),
            ("Upright", "plate_1"),  # check if the plate is upright
        ]
    )
    
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
