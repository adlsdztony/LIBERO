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
    language = "Arrange the plate perpendicular to the cabinet front"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "plate_1",
],
        goal_states=[
        ("AxisAlignedWithin", "plate_1", "z", 75, 105),
        ("axisalignedwithinworldaxis", "plate_1", "z", 75, 105, "y"),
        ("Any", (
            ("axisalignedwithinworldaxis", "plate_1", "z", 0, 10, "x"),
            ("axisalignedwithinworldaxis", "plate_1", "z", 170, 180, "x"),
        )),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
