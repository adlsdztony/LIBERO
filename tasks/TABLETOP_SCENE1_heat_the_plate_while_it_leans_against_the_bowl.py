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
    language = "Heat the plate while it leans against the bowl"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "plate_1",
    "akita_black_bowl_1",
    "flat_stove_1"
],
        goal_states=[
        ("InContact", "plate_1", "akita_black_bowl_1"),
        ("FlexibleAbove", "plate_1", "flat_stove_1_cook_region", 0.06),
        ("Any", (
            ("AxisAlignedWithin", "plate_1", "x", 20, 80),
            ("AxisAlignedWithin", "plate_1", "x", 100, 170),
            ("AxisAlignedWithin", "plate_1", "y", 20, 80),
            ("AxisAlignedWithin", "plate_1", "y", 100, 170),
        )),
        ("AxisAlignedWithin", "plate_1", "z", 0, 90),
        ("TurnOn", "flat_stove_1"),
        ("Not",  ("InContact", "gripper0_finger1_pad", "plate_1")),
        ("Not",  ("InContact", "gripper0_finger2_pad", "plate_1")),
        ("Not",  ("InContact", "gripper0_finger1", "plate_1")),
        ("Not",  ("InContact", "gripper0_finger2", "plate_1")),
        ("Not",  ("InContact", "gripper0_hand", "plate_1")),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
