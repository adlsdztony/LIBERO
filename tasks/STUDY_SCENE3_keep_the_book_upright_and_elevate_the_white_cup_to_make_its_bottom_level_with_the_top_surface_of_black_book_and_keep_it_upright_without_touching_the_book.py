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

    scene_name = "study_scene3"
    language = "Keep the book upright and elevate the white cup to make its bottom level with the top surface of black book and keep it upright without touching the book"
    pos_range = [0, 0, 1]
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "black_book_1"],
        goal_states=[
            ("AxisAlignedWithin", "black_book_1", "z", 0, 5),
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 0, 5),
            ("PositionWithin", "porcelain_mug_1", pos_range[0], pos_range[1], pos_range[2], 1, 1, 0.02),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
