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

from libero.libero.benchmark.mu_creation_dynamic import *

def main():

    scene_name = "living_room_scene12"
    language = "Place the orange juice tilted at an angle next to the basket"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["orange_juice_1", "basket_1"],
        goal_states=[
            ("InContact", "orange_juice_1", "basket_1"),
            ("AxisAlignedWithin", "orange_juice_1", "y", 30, 60),
            ("On", "orange_juice_1", "living_room_table_table_region"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
