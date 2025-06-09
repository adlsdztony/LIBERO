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

    # Write your reward code here
    scene_name = "kitchen_scene6"
    language = "Put the white-and-yellow mug in the microwave,close the microwave, and put the porcelain mug on the microwave. Keep both mug upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["microwave_1", "porcelain_mug_1", "white_yellow_mug_1"],
        goal_states=[
            ("In", "white_yellow_mug_1", "microwave_1_heating_region"),
            ("PositionWithinObject", "porcelain_mug_1", "microwave_1", -0.16, -0.07, 0.18, 0.05, 0.13, 0.19),
            ("Equal", ("GetPosi", "porcelain_mug_1", "z"), 1.10, 0.01),
            ("Close", "microwave_1"),
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 0, 5),
            ("AxisAlignedWithin", "white_yellow_mug_1", "z", 0, 5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
