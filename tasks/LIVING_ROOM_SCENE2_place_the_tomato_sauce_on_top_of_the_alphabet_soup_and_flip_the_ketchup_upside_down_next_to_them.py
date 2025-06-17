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
    language = "Rearrage the objects so that the ketchup, flipped upside down, is placed directly beside the tomato sauce stacked on top of the alphabet soup, in contact with either one of them"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["alphabet_soup_1", "tomato_sauce_1", "ketchup_1"],
        goal_states=[
            ("On", "tomato_sauce_1", "alphabet_soup_1"),
            ("AxisAlignedWithin", "ketchup_1", "y", 170, 180),
            ("Equal", ("GetPosi", "ketchup_1", "z"), 0.510, 0.001),
            ("Equal", ("GetPosi", "alphabet_soup_1", "z"), 0.475, 0.001),
            ("Or",
                ("InContact", "tomato_sauce_1", "ketchup_1"),
                ("InContact", "alphabet_soup_1", "ketchup_1")
            )
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
