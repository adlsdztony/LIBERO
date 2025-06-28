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

    scene_name = "kitchen_scene8"
    language = "Turn off stove and lift right moka pot upright in air."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["flat_stove_1", "moka_pot_2"],
        goal_states=[
            ("TurnOff", "flat_stove_1"),
            ("InAir",   "moka_pot_2", 1.0),
            ("Upright", "moka_pot_2"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
