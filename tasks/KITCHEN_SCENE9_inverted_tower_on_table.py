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

from libero.libero.benchmark.mu_creation_dynamic import *

def main():

    scene_name = "kitchen_scene9"
    language = "Create an inverted tower on the table with the bowl as base upside down and frypan on top upright"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["white_bowl_1", "chefmate_8_frypan_1", "wooden_two_layer_shelf_1"],
        goal_states=[
            ("UpsideDown", "white_bowl_1"),
            ("On", "chefmate_8_frypan_1", "white_bowl_1"),
            ("Upright", "chefmate_8_frypan_1"),
            ("On", "white_bowl_1", "kitchen_table_table_region"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
