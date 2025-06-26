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

from libero.libero.benchmark.mu_creation import LivingRoomScene3

def main():

    scene_name = "living_room_scene2"
    language = "First turn the tomato can upside down, then place the butter on top, then cover both with the basket"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1", "basket_1", "tomato_sauce_1"],
        goal_states=[
            ("AxisAlignedWithin", "tomato_sauce_1", "y", 175, 180),
            ("RelaxedOn", "butter_1", "tomato_sauce_1"),
            ("In", "tomato_sauce_1", "basket_1_contain_region"),
            ("In", "butter_1", "basket_1_contain_region"),
            ("UpsideDown", "basket_1"),
            ("PositionWithin", "basket_1", 0.0, 0.0, 0.582, 1, 1, 0.01),
            ("PositionWithin", "tomato_sauce_1", 0.0, 0.0, 0.474, 1, 1, 0.02),
            ("PositionWithin", "butter_1", 0.0, 0.0, 0.521, 1, 1, 0.02),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
