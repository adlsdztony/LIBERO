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

    scene_name = "kitchen_scene9"
    language = "Stack both items on the shelf bottom with the frypan upright and bowl upright in it"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chefmate_8_frypan_1", "white_bowl_1", "wooden_two_layer_shelf_1"],
        goal_states=[
            ("In", "chefmate_8_frypan_1", "wooden_two_layer_shelf_1_bottom_region"),
            ("Upright", "chefmate_8_frypan_1"),
            ("On", "white_bowl_1", "chefmate_8_frypan_1"),
            ("Upright", "white_bowl_1"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
