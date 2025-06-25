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
    language = "Place the wine bottle on the heated stove with the neck pointing left"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "wine_bottle_1",
    "flat_stove_1"
],
        goal_states=[
        ("FlexibleAbove", "wine_bottle_1", "flat_stove_1_cook_region", 0.07),
        ("InContact", "wine_bottle_1", "flat_stove_1"),
        ("TurnOn", "flat_stove_1"),
        ("Any", (
            ("OrientedAtDegree", "wine_bottle_1",   90.03,   5.38, -175.10,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -90.52,  86.48,    1.15,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -90.52,  86.48,   -0.17,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -91.71, -88.93,    5.81,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -90.03,   2.92,    0.73,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -90.03,   2.92,    2.21,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -91.71, -88.93,    5.46,  2.0,  5.0, 10.0),
            ("OrientedAtDegree", "wine_bottle_1",  -90.52,  86.48,    5.97,  2.0,  5.0, 10.0),
        )),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
