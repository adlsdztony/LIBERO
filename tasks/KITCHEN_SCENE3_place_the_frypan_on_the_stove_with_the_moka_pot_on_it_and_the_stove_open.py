"""This is a standalone file for create a task in libero."""
from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)
import numpy as np

from libero.libero.benchmark.mu_creation import KitchenScene3

def main():
    scene_name = "kitchen_scene3"
    language = "Place the frypan on the stove with the moka pot on it and the stove open"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["flat_stove_1", "chefmate_8_frypan_1","moka_pot_1"],
        goal_states=[
            ("relaxedon", "moka_pot_1", "chefmate_8_frypan_1"),
            ("Upright", "moka_pot_1"),
            ("On", "chefmate_8_frypan_1", "flat_stove_1_cook_region"),
            ("TurnOn", "flat_stove_1")
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()