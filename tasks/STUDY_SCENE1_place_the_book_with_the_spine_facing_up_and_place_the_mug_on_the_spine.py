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

from libero.libero.benchmark.mu_creation import StudyScene1

def main():

    scene_name = "study_scene1"
    language = "Place the book with the spine facing up and place the mug on the spine"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["black_book_1", "white_yellow_mug_1"],
        goal_states=[
            # Book’s spine pointing upward
            ("AxisAlignedWithin", "black_book_1", "y", 0, 5),
            # Mug resting on the spine
            ("Under", "black_book_1", "white_yellow_mug_1"),
            ("InContact", "black_book_1", "white_yellow_mug_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
