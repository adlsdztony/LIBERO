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
    language = "Place the bowl into the top drawer located in the drawer's bottom right corner"
    # x-y center of cabinet is 0, -0.3 (from the init_state of the scene)
    # known from teleoperation and printing out the current position
    # then calculate the target position
    bottom_right_corner = [-0.05, -0.25, 1.06]
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1"],
        goal_states=[
            ("PositionWithin", "akita_black_bowl_1", bottom_right_corner[0], bottom_right_corner[1], bottom_right_corner[2], 0.015, 0.05, 0.01),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
