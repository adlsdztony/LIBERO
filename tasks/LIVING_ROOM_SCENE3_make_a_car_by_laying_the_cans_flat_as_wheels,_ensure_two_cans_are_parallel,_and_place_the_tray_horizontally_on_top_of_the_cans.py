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
    scene_name = "living_room_scene3"
    language = "Make a car by laying the cans flat as wheels, ensure two cans are parallel, and place the tray horizontally on top of the cans"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_tray_1", "alphabet_soup_1", "tomato_sauce_1"],
        goal_states=[
            ("AxisAlignedWithinWorldAxis", "alphabet_soup_1", "y", 85, 95, "z"),
            ("AxisAlignedWithinWorldAxis", "tomato_sauce_1", "y", 85, 95, "z"),
            ("Or", 
                ("AxisAlignedWithinObjectAxis", "alphabet_soup_1", "tomato_sauce_1", "y", "y", 0, 10),
                ("AxisAlignedWithinObjectAxis", "alphabet_soup_1", "tomato_sauce_1", "y", "y", 170, 180)
            ),
            ("PosiLessThan", "tomato_sauce_1", "z", 0.474),
            ("PosiLessThan", "alphabet_soup_1", "z", 0.474),
            ("RelaxedOn", "wooden_tray_1", "alphabet_soup_1"),
            ("RelaxedOn", "wooden_tray_1", "tomato_sauce_1"),
            ("AxisAlignedWithin", "wooden_tray_1", "z", 0, 10),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
