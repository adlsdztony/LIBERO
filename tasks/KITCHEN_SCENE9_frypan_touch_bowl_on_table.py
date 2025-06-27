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
    language = "Position the frypan to touch the bowl while both are on the table surface"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chefmate_8_frypan_1", "white_bowl_1", "wooden_two_layer_shelf_1"],
        goal_states=[
            ("InContact", "chefmate_8_frypan_1", "white_bowl_1"),
            ("On", "chefmate_8_frypan_1", "kitchen_table_table_region"),
            ("On", "white_bowl_1", "kitchen_table_table_region"),
            ("PositionWithin", "white_bowl_1", -0.142, 0.090, 0.899, 0.1, 0.1, 0.1),
            ("Not", ("On", "chefmate_8_frypan_1", "wooden_two_layer_shelf_1")),
            ("Not", ("On", "white_bowl_1", "wooden_two_layer_shelf_1")),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
