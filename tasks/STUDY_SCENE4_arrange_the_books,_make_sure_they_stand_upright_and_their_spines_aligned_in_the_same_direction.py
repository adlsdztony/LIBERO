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

    scene_name = "study_scene4"
    language = "Arrange the books, make sure they stand upright and their spines aligned in the same direction"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["black_book_1", "yellow_book_1", "yellow_book_2"],
        goal_states=[
            ("Upright", "black_book_1"),
            ("Upright", "yellow_book_1"),
            ("Upright", "yellow_book_2"),
            ("AxisAlignedWithinObjectAxis", "black_book_1", "yellow_book_1", "y", "y", 0, 10),
            ("AxisAlignedWithinObjectAxis", "yellow_book_1", "yellow_book_2", "y", "y", 0, 10),
            ("AxisAlignedWithinObjectAxis", "black_book_1", "yellow_book_2", "y", "y", 0, 10),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
