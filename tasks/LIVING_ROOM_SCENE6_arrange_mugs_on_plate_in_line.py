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

    scene_name = "living_room_scene6"
    language = "arrange the two mugs on the plate in a line with the porcelain mug on the left and red mug on the right"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
            "porcelain_mug_1",
            "red_coffee_mug_1",
            "plate_1",
            "chocolate_pudding_1",
        ],
        goal_states=[
            ("FlexibleOn", "porcelain_mug_1", "plate_1", 0.075, 0.075),
            ("FlexibleOn", "red_coffee_mug_1", "plate_1", 0.075, 0.075),
            ("LROrdering", "red_coffee_mug_1", "plate_1", "porcelain_mug_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
