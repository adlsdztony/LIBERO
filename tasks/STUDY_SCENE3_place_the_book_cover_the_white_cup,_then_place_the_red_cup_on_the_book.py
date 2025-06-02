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
    language = "Place the book cover the white cup, then place the red cup on the book"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "red_coffee_mug_1", "black_book_1"],
        goal_states=[
            ("Under", "black_book_1", "red_coffee_mug_1"),
            ("InContact", "black_book_1", "red_coffee_mug_1"),
            ("Under", "porcelain_mug_1", "black_book_1"),
            ("InContact", "porcelain_mug_1", "black_book_1"),
            ("AxisAlignedWithin", "black_book_1", "z", 88, 92),
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 0, 5),
            ("AxisAlignedWithin", "red_coffee_mug_1", "z", 0, 5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
