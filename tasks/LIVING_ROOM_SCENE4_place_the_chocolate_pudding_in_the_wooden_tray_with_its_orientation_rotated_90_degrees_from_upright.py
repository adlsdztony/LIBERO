"""This is a standalone file for create a task in libero."""
import numpy as np

from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
    get_task_info
)

from libero.libero.benchmark.mu_creation import *


def main():
    # living_room_scene_4
    scene_name = "living_room_scene4"
    language = "Place the chocolate pudding in the wooden tray with its orientation rotated 90 degrees from upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chocolate_pudding_1"],
        goal_states=[
            ('In', 'chocolate_pudding_1', 'wooden_tray_1_contain_region'),
            ('AxisAlignedWithin', 'chocolate_pudding_1', 'z', '85', '95')
        ],
    )


    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
