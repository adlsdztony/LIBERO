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
    language = "Position the milk in the basket upside down with its side against the right wall"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1", "basket_1"],
        goal_states=[
            ("In", "milk_1", "basket_1_contain_region"),
            ("InContact", "milk_1", "basket_1"),
            ("AxisAlignedWithin", "milk_1", "y", 100, 175),
            ("AxisAlignedWithinWorldAxis", "milk_1", "y", 10, 80, "y"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
