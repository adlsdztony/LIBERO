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
    language = "Lift the cream cheese and stand it on its corner"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "cream_cheese_1"
],
        goal_states=[
        ("ConstraintOnce", ("InAir", "cream_cheese_1", 0.91)),
        ("Not",  ("InContact", "gripper0_finger1_pad", "cream_cheese_1")),
        ("Not",  ("InContact", "gripper0_finger2_pad", "cream_cheese_1")),
        ("Not",  ("InContact", "gripper0_finger1", "cream_cheese_1")),
        ("Not",  ("InContact", "gripper0_finger2", "cream_cheese_1")),
        ("Not",  ("InContact", "gripper0_hand", "cream_cheese_1")),
        ("Any", (
    ("OrientedAtDegree", "cream_cheese_1",  59.11, -38.47, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1", 133.99, -46.84, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1", -58.47, -47.85, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1", -138.11, -54.32, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1", -123.92,  41.67, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1",  -55.29,  47.14, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1", -133.27,  40.53, 0, 15.0, 15.0, 180),
    ("OrientedAtDegree", "cream_cheese_1",  -56.38,  53.04, 0, 15.0, 15.0, 180),
        )),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
