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

    scene_name = "living_room_scene5"
    language = "Place the red coffee mug on the right plate with the mug lying on its side"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["red_coffee_mug_1", "plate_1"],
        goal_states=[
            ("RelaxedOn", "red_coffee_mug_1", "plate_1"),
            ("AxisAlignedWithIn", "red_coffee_mug_1", "z", 80, 100),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
