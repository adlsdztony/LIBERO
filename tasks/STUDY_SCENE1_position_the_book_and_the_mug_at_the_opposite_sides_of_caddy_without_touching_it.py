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
    language = "Position the book and the mug at the opposite sides of caddy without touching it"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "black_book_1",
    "white_yellow_mug_1",
    "desk_caddy_1"
],
        goal_states=[
        ("Not", ("InContact", "black_book_1", "desk_caddy_1")),
        ("Not", ("InContact", "white_yellow_mug_1", "desk_caddy_1")),
        ("Any", (
            ("All", (
                ("PosiGreaterThan", "black_book_1", "y", 0.06),
                ("PosiGreaterThan", "black_book_1", "x", -0.49),
                ("PosiLessThan", "black_book_1", "x", -0.32),
                ("PosiLessThan", "white_yellow_mug_1", "y", -0.33),
                ("PosiGreaterThan", "white_yellow_mug_1", "x", -0.49),
                ("PosiLessThan", "white_yellow_mug_1", "x", -0.32),
            )),
            ("All", (
                ("PosiGreaterThan", "white_yellow_mug_1", "y", 0.06),
                ("PosiGreaterThan", "white_yellow_mug_1", "x", -0.49),
                ("PosiLessThan", "white_yellow_mug_1", "x", -0.32),
                ("PosiLessThan", "black_book_1", "y", -0.33),
                ("PosiGreaterThan", "black_book_1", "x", -0.49),
                ("PosiLessThan", "black_book_1", "x", -0.32),
            )),
            ("All", (
                ("PosiLessThan", "black_book_1", "x", -0.46),
                ("PosiGreaterThan", "black_book_1", "y", -0.34),
                ("PosiLessThan", "black_book_1", "y", 0.06),
                ("PosiGreaterThan", "white_yellow_mug_1", "x", -0.32),
                ("PosiGreaterThan", "white_yellow_mug_1", "y", -0.34),
                ("PosiLessThan", "white_yellow_mug_1", "y", 0.06),
            )),
            ("All", (
                ("PosiLessThan", "white_yellow_mug_1", "x", -0.46),
                ("PosiGreaterThan", "white_yellow_mug_1", "y", -0.34),
                ("PosiLessThan", "white_yellow_mug_1", "y", 0.06),
                ("PosiGreaterThan", "black_book_1", "x", -0.32),
                ("PosiGreaterThan", "black_book_1", "y", -0.34),
                ("PosiLessThan", "black_book_1", "y", 0.06),
            )),
        )),
        ("Not", ("InContact", "gripper0_finger1", "white_yellow_mug_1")),
        ("Not", ("InContact", "gripper0_finger2", "white_yellow_mug_1")),
        ("Not", ("InContact", "gripper0_hand", "white_yellow_mug_1")),
        ("Not", ("InContact", "gripper0_finger1_pad", "white_yellow_mug_1")),
        ("Not", ("InContact", "gripper0_finger2_pad", "white_yellow_mug_1")),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
