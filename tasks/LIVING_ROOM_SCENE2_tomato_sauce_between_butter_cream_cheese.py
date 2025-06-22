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
    language = "Position the tomato sauce on the table between the butter and cream cheese and stay in contact with both"
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["tomato_sauce_1", "butter_1", "cream_cheese_1"],
        goal_states=[
            ("Or",
                ("MidBetween", "butter_1", "tomato_sauce_1", "cream_cheese_1", "y"),
                ("MidBetween", "cream_cheese_1", "tomato_sauce_1", "butter_1", "x")
            ),
            ("On", "tomato_sauce_1", "living_room_table_table_region"),
            ("On", "butter_1", "living_room_table_table_region"),
            ("On", "cream_cheese_1", "living_room_table_table_region"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
