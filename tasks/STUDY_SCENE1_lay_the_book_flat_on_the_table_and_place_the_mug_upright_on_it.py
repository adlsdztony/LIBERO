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
    language = "Lay the book flat on the table and place the mug upright on it"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "desk_caddy_1",
    "black_book_1",
    "white_yellow_mug_1"
],
        goal_states=[
        ("Or", ("AxisAlignedWithin", "black_book_1", 'x', 175, 180), ("AxisAlignedWithin", "black_book_1", 'x', 0, 5)),
        ("AxisAlignedWithin", "black_book_1", 'y', 85, 95),
        ("AxisAlignedWithin", "black_book_1", 'z', 85, 95),
        ("Upright", "white_yellow_mug_1"),
        ("RelaxedOn", "white_yellow_mug_1", "black_book_1"),
        ("Not", ("InAir", "black_book_1", 0.90)),
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
