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
    language = "Lay the basket on its side, place the cream cheese upright on top of the side surface, and position the alphabet soup underneath the basket."
    
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["basket_1", "cream_cheese_1", "alphabet_soup_1"],
        goal_states=[
            ("PosiGreaterThan", "cream_cheese_1", "z", 0.67),
            ("UpRight", "cream_cheese_1"),
            ("Under", "alphabet_soup_1", "basket_1"),
            ("AxisAlignedWithin", "basket_1", "z", 80, 100),
            ("incontact", "cream_cheese_1", "basket_1"),
            ("incontact", "alphabet_soup_1", "basket_1"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
