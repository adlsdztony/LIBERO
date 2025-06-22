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
    language = "turn on the stove and place the upright bowl directly on the burner"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["flat_stove_1", "white_bowl_1", "chefmate_8_frypan_1"],
        goal_states=[
            ("TurnOn", "flat_stove_1"),
            ("On", "white_bowl_1", "flat_stove_1_cook_region"),
            ("Upright", "white_bowl_1"),
            ("Not", ("RelaxedOn", "white_bowl_1", "chefmate_8_frypan_1")),
            ("Not", ("On", "chefmate_8_frypan_1", "flat_stove_1_cook_region")),
            ("Not", ("InContact", "white_bowl_1", "chefmate_8_frypan_1")),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
