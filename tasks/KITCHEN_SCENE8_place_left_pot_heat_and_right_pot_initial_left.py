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
    language = "place left pot on cook region and right pot on left pot's initial position"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["moka_pot_1", "flat_stove_1", "moka_pot_2"],
        goal_states=[
            ("On", "moka_pot_1", "flat_stove_1_cook_region"),
            ("On", "moka_pot_2", "kitchen_table_moka_pot_right_init_region"),
            ("Upright", "moka_pot_1"),
            ("Upright", "moka_pot_2"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
