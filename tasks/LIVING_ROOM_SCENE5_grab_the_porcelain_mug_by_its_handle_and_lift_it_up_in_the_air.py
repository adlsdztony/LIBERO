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

    scene_name = "living_room_scene5"
    language = "Grab the porcelain mug by its handle and lift it up in the air"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1"],
        goal_states=[
            ("InAir", "porcelain_mug_1", 0.52),
            ("InContact", "porcelain_mug_1", "gripper0_finger1_pad"),
            ("InContact", "porcelain_mug_1", "gripper0_finger2_pad"),
            ("GreaterThan", ("PlanarDistance", "gripper0_hand", "porcelain_mug_1"), 0.024),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
