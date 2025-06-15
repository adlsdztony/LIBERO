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

from libero.libero.benchmark.mu_creation import KitchenScene3

def main():

    scene_name = "kitchen_scene3"
    language = "Place the moka pot on the stove with its handle pointing toward the front of the table, and turn on the stove"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["flat_stove_1", "moka_pot_1"],
        goal_states=[
            ("On", "moka_pot_1", "flat_stove_1_cook_region"),
            ("OrientedAtDegree", "moka_pot_1", 0, 0, -90, 5, 5, 10),
            ("TurnOn", "flat_stove_1"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
