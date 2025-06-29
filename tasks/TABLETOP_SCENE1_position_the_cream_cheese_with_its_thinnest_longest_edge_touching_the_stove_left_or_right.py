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
    language = "Position the cream cheese with its thinnest longest edge touching the stove from the left or right"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "cream_cheese_1",
    "flat_stove_1"
],
        goal_states=[
        ("InContact", "cream_cheese_1", "flat_stove_1"),
        ("Any", (
            ("All", (
                ("PosiLessThanObject", "cream_cheese_1", "flat_stove_1", "y", 0.05),
                ("PositionWithin", "cream_cheese_1", -0.26, 0, 0.9, 0.08, 10, 10)
            )),
            ("All", (
                ("PosiGreaterThanObject", "cream_cheese_1", "flat_stove_1", "y", 0.05),
                ("PositionWithin", "cream_cheese_1", -0.28, 0, 0.9, 0.07, 10, 10)
            )),
        )),
        ("Not", ("InAir", "cream_cheese_1", 0.91)),
        ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "y", 85, 95, "x"),
        ("Or", 
            ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "z", 0, 5, "z"),
            ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "z", 175, 180, "z"),
        ),
        ("Or", 
            ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "x", 0, 5, "x"),
            ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "x", 175, 180, "x"),
        ),        
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
