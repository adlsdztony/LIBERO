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

    scene_name = "kitchen_scene11"
    language = "Collect all the white bowls from the cabinet and stack them on the plate"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[],
        goal_states=[
            ("Or", ("StackBowl", "white_bowl_1", "white_bowl_2"), ("StackBowl", "white_bowl_1", "white_bowl_3")),
            ("Or", ("StackBowl", "white_bowl_2", "white_bowl_3"), ("StackBowl", "white_bowl_2", "white_bowl_1")),
            ("Or", ("StackBowl", "white_bowl_3", "white_bowl_1"), ("StackBowl", "white_bowl_3", "white_bowl_2")),
            ("Or", ("On", "white_bowl_1", "plate_1"), ("Or", ("On", "white_bowl_2", "plate_1"), ("On", "white_bowl_3", "plate_1"))),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
