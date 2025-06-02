"""This is a standalone file for create a task in libero."""
from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)
import numpy as np

from libero.libero.benchmark.mu_creation import StudyScene3

def main():
    # study_scene3
    scene_name = "study_scene3"
    language = "Position the book so it creates a bridge between the two cups"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "black_book_1", "red_coffee_mug_1"],
        goal_states=[
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 0, 5),
            ("AxisAlignedWithin", "red_coffee_mug_1", "z", 0, 5),
            ("Under", "porcelain_mug_1", "black_book_1"),
            ("Under", "red_coffee_mug_1", "black_book_1"),
            ("InContact", "porcelain_mug_1", "black_book_1"),
            ("InContact", "red_coffee_mug_1", "black_book_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
