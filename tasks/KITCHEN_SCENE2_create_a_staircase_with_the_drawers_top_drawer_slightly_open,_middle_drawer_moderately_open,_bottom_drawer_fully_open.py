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
    # kitchen_scene_2
    scene_name = "kitchen_scene2"
    language = "Create a staircase with the drawers: top drawer slightly open, middle drawer moderately open, bottom drawer fully open"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_cabinet_1"],
        goal_states=[
            ("StairCase", "wooden_cabinet_1_top_region", "wooden_cabinet_1_middle_region", "wooden_cabinet_1_bottom_region")
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
