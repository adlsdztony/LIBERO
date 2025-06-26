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

    scene_name = "living_room_scene2"
    language = "Place both the milk and alphabet soup in the basket with the milk standing upright"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1", "alphabet_soup_1", "basket_1"],
        goal_states=[
            ("In", "milk_1", "basket_1_contain_region"),
            ("In", "alphabet_soup_1", "basket_1_contain_region"),
            ("AxisAlignedWithin", "milk_1", "y", 0, 5),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
