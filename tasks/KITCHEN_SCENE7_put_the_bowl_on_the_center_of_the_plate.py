"""This is an exmaple file for creating a task in libero."""
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
    # kitchen_scene_1
    scene_name = "kitchen_scene7"
    language = "Put the bowl on the center of the plate"
    center_threshold = 0.015 # 1.5cm from the center of the plate
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["white_bowl_1", "plate_1"],
        goal_states=[
            ("ThresholdOn", "white_bowl_1", "plate_1", center_threshold),
        ],
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
