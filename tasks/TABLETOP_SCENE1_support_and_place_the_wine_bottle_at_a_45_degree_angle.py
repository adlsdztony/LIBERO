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
    language = "Support and place the wine bottle at a 45-degree angle"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "wine_bottle_1",
],
        goal_states=[
        ("Any", (
            ("AxisAlignedWithin", "wine_bottle_1", "x", 40, 50),
            ("AxisAlignedWithin", "wine_bottle_1", "x", 130, 140),
            ("AxisAlignedWithin", "wine_bottle_1", "y", 40, 50),
            ("AxisAlignedWithin", "wine_bottle_1", "y", 130, 140),
        )),
        ("AxisAlignedWithin", "plate_1", "z", 0, 90),
        ("Not",  ("InContact", "gripper0_finger1_pad", "wine_bottle_1")),
        ("Not",  ("InContact", "gripper0_finger2_pad", "wine_bottle_1")),
        ("Not",  ("InContact", "gripper0_finger1", "wine_bottle_1")),
        ("Not",  ("InContact", "gripper0_finger2", "wine_bottle_1")),
        ("Not",  ("InContact", "gripper0_hand", "wine_bottle_1")),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
