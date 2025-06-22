"""This is a standalone file for creating a task in libero."""
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

    # Write your reward code here
    scene_name = "kitchen_scene6"
    language = "Balance porcelain mug horizontally on top of white-and-yellow mug"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "white_yellow_mug_1"],
        goal_states=[
            ("RelaxedOn", "porcelain_mug_1", "white_yellow_mug_1"),
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 80, 100),
            ("AxisAlignedWithin", "white_yellow_mug_1", "z", 0, 5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
