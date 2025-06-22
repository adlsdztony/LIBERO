"""This is a standalone file for creating a task in libero."""
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

    scene_name = "kitchen_scene7"
    language = "Pick up the plate and balance it on the bowl"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["microwave_1", "white_bowl_1", "plate_1"],
        goal_states=[
            ("RelaxedOn", "plate_1", "white_bowl_1"),
            ("Not", ("InContact", "plate_1", "microwave_1")),
            ("AxisAlignedWithin", "plate_1", "z", 0, 5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
