"""This is a standalone file for create a task in libero."""
from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)
import numpy as np

from libero.libero.benchmark.mu_creation import LivingRoomScene5

def main():
    scene_name = "living_room_scene5"
    language = "Arrange the three mugs so the porcelain mug is between the other two mugs along the table length"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[ "red_coffee_mug_1","porcelain_mug_1","white_yellow_mug_1"],
        goal_states=[
            ("between", "red_coffee_mug_1", "porcelain_mug_1", "white_yellow_mug_1", "y")
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()