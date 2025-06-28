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

from libero.libero.benchmark.mu_creation import LivingRoomScene2

def main():

    scene_name = "living_room_scene2"
    language = "Arrange the milk and orange juice in a straight line with the basket positioned between them"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1", "basket_1", "orange_juice_1"],
        goal_states=[
            ("RelaxedBetween", "milk_1", "basket_1", "orange_juice_1", "y"),
            ("Linear", "milk_1", "basket_1", "orange_juice_1", 0.001),
            ("Not", ("DistanceBetween", "milk_1", "basket_1", 0.061, 0.061, 0.1)),
            ("Not",("In", "milk_1", "basket_1_contain_region"),),
            ("Not",("In", "orange_juice_1", "basket_1_contain_region"),),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
