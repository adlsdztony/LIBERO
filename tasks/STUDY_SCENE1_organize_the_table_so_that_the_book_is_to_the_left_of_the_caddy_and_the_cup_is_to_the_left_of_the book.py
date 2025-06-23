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
    language = "Organize the table so that the book is to the left of the caddy and the cup is to the left of the book"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["desk_caddy_1", "white_yellow_mug_1","black_book_1"],
        goal_states=[
        # Objects placed from left to right: cup, book, then caddy
        ("OrderAlongAxis", "y", "white_yellow_mug_1", "black_book_1", "desk_caddy_1"),
        # Keep them roughly aligned in depth (x-axis)
        ("PosiSameWith", "white_yellow_mug_1", "black_book_1", "x", 0.02),
        ("PosiSameWith", "black_book_1", "desk_caddy_1", "x", 0.02),
        ("Not", ("InAir", "black_book_1", 0.89)),
        ("Not", ("InAir", "white_yellow_mug_1", 0.89)),
    ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()