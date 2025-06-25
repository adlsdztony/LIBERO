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
    language = "Cook with the bowl tilted at an angle on the stove"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "akita_black_bowl_1",
    "flat_stove_1"
],
        goal_states=[
        ("Above", "akita_black_bowl_1", "flat_stove_1_cook_region"),
        ("InContact", "akita_black_bowl_1", "flat_stove_1"),
        ("Any", (
            ("AxisAlignedWithin", "akita_black_bowl_1", "x", 20, 80),
            ("AxisAlignedWithin", "akita_black_bowl_1", "x", 100, 170),
            ("AxisAlignedWithin", "akita_black_bowl_1", "y", 20, 80),
            ("AxisAlignedWithin", "akita_black_bowl_1", "y", 100, 170),
        )),
        ("AxisAlignedWithin", "akita_black_bowl_1", "z", 0, 90),
        ("TurnOn", "flat_stove_1")
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
