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
    language = "Place the wine bottle on the table with the neck pointing toward the plate"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "wine_bottle_1",
    "plate_1"
],
        goal_states=[
        ("Not", ("InAir", "wine_bottle_1", 0.925)), 
        ("Not", ("InContact", "wine_bottle_1", "plate_1")),
        ("IsFacingObject", "wine_bottle_1", "plate_1", 0, 0, 1, 13),
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
