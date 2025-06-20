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
    """Defines and registers the task with the libero environment."""
    scene_name = "study_scene1"
    language = "Place the book on the table, leaning against the side of the caddy"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "desk_caddy_1",
    "black_book_1",
],
        goal_states=[
        ("IsTouchingSideAxis", "black_book_1", "desk_caddy_1", "y", 0.6),
        ("DistanceBetween", "black_book_1", "desk_caddy_1", 0.06, 10, 10),
        ("Not",    
            ("Any",(
                ("In", "black_book_1", "desk_caddy_1_left_contain_region"),
                ("In", "black_book_1", "desk_caddy_1_front_contain_region"),
                ("In", "black_book_1", "desk_caddy_1_back_contain_region"),
                ("In", "black_book_1", "desk_caddy_1_right_contain_region"),
            ))),
        ("Not", ("InContact", "gripper0_finger1", "black_book_1")),
        ("Not", ("InContact", "gripper0_finger2", "black_book_1")),
        ("Not", ("InContact", "gripper0_hand", "black_book_1")),
        ("Not", ("InContact", "gripper0_finger1_pad", "black_book_1")),
        ("Not", ("InContact", "gripper0_finger2_pad", "black_book_1")),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
