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
    language = "Place the tomato sauce on top of the alphabet soup and flip the ketchup upside down next to them"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["alphabet_soup_1", "cream_cheese_1", "basket_1"],
        goal_states=[
            ("On", "tomato_sauce_1", "alphabet_soup_1"),
            ("AxisAlignedWithin", "ketchup_1", "y", 170, 180),
            ("PositionWithinObjectAnnulus", "ketchup_1", "tomato_sauce_1", 0.04, 0.1),
            ("PositionWithinObjectAnnulus", "ketchup_1", "alphabet_soup_1", 0.04, 0.1),
            ("Equal", ("GetPosi", "ketchup_1", "z"), 0.509, 0.001),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
