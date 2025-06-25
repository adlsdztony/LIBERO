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
    scene_name = "tabletop_scene1"
    language = "Touch both the cream cheese and plate simultaneously with different robot fingers"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "cream_cheese_1",
    "plate_1"
],
        goal_states=[
    ("Any", (
        ("All", (
            ("InContact", "gripper0_finger1",    "cream_cheese_1"),
            ("InContact", "gripper0_finger2",    "plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger1",    "cream_cheese_1"),
            ("InContact", "gripper0_finger2_pad","plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger2",    "cream_cheese_1"),
            ("InContact", "gripper0_finger1",    "plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger2",    "cream_cheese_1"),
            ("InContact", "gripper0_finger1_pad","plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger1_pad","cream_cheese_1"),
            ("InContact", "gripper0_finger2",    "plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger1_pad","cream_cheese_1"),
            ("InContact", "gripper0_finger2_pad","plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger2_pad","cream_cheese_1"),
            ("InContact", "gripper0_finger1",    "plate_1"),
        )),
        ("All", (
            ("InContact", "gripper0_finger2_pad","cream_cheese_1"),
            ("InContact", "gripper0_finger1_pad","plate_1"),
        )),
    )),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
