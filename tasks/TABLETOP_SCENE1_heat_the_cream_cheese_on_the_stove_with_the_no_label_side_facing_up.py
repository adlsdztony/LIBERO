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
    language = "Heat the cream cheese on the stove with the no label side facing up"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "cream_cheese_1",
    "flat_stove_1"
],
        goal_states=[
        ("FlexibleAbove", "cream_cheese_1", "flat_stove_1_cook_region", 0.03),
        ("InContact", "cream_cheese_1", "flat_stove_1"),
        ("TurnOn", "flat_stove_1"),
        ("OrientedAtDegree", "cream_cheese_1", -90, 0, 0, 0.5, 0.5, 180),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
