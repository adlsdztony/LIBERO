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
    language = "Pick up the plate and place it leaning against the upright wine bottle"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "plate_1",
    "wine_bottle_1"
],
        goal_states=[
        ("InContact", "plate_1", "wine_bottle_1"),
        ("Not", ("InAir", "wine_bottle_1", 0.90)),
        ("Upright", "wine_bottle_1"),
        ("Any", (
            ("AxisAlignedWithin", "plate_1", "x", 20, 80),
            ("AxisAlignedWithin", "plate_1", "x", 100, 170),
            ("AxisAlignedWithin", "plate_1", "y", 20, 80),
            ("AxisAlignedWithin", "plate_1", "y", 100, 170),
        )),
        ("AxisAlignedWithin", "plate_1", "z", 0, 90),
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
