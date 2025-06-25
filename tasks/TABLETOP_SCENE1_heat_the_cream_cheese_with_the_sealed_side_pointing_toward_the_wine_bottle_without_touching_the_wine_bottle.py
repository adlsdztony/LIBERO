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
    language = "Heat the cream cheese with the sealed side pointing toward the wine bottle without touching the wine bottle"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "cream_cheese_1",
    "flat_stove_1"
],
        goal_states=[
        ("ConstraintNever", ("InContact", "wine_bottle_1", "gripper0_finger1_pad")),
        ("ConstraintNever", ("InContact", "wine_bottle_1", "gripper0_finger2_pad")),
        ("ConstraintNever", ("InContact", "wine_bottle_1", "gripper0_finger1")),
        ("ConstraintNever", ("InContact", "wine_bottle_1", "gripper0_finger2")),
        ("ConstraintNever", ("InContact", "wine_bottle_1", "gripper0_hand")),
        ("FlexibleAbove", "cream_cheese_1", "flat_stove_1_cook_region", 0.03),
        ("TurnOn", "flat_stove_1"),
        ("InContact", "cream_cheese_1", "flat_stove_1"),
        ("Any", (
            ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "x", 0, 15, "y"),
            ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "x", 165, 180, "y"),
        )),       
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
