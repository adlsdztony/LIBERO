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
    language = "create a double-stacked configuration use the bowl and teh frypan on the top shelf with both items upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chefmate_8_frypan_1", "wooden_two_layer_shelf_1", "white_bowl_1", "flat_stove_1"],
        goal_states=[
            ("RelaxedOn", "chefmate_8_frypan_1", "wooden_two_layer_shelf_1"),
            ("Upright", "chefmate_8_frypan_1"),
            ("RelaxedOn", "white_bowl_1", "chefmate_8_frypan_1"),
            ("Upright", "white_bowl_1"),
            ("Under", "chefmate_8_frypan_1", "white_bowl_1"),
            ("Not", ("RelaxedOn", "white_bowl_1", "wooden_two_layer_shelf_1")),
            ("Not", ("RelaxedOn", "chefmate_8_frypan_1", "flat_stove_1")),
            ("Not", ("RelaxedOn", "white_bowl_1", "flat_stove_1")),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main() 