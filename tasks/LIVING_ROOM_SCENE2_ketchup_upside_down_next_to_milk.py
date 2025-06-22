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
    language = "Place the ketchup upside down touching the upright milk on the table"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "milk_1"],
        goal_states=[
            ("AxisAlignedWithin", "ketchup_1", "y", 170, 180),
            ("InContact", "ketchup_1", "milk_1"),
            ("AxisAlignedWithin", "milk_1", "y", 0, 10),
            ("PosiLessThan", "ketchup_1", 'z', 0.512),
            ("PosiLessThan", "milk_1", 'z', 0.51),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
