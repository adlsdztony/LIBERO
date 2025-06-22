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
    language = "Lay all items flat in the tray and ensure them touching the bottom of the tray"
    # wooden_tray_z = 0.43738009
    # laid_butter_z = 0.45281869
    # laid_ketchup_z = 0.46391021
    # laid_tomato_sauce_z = 0.47818113
    # butter_height = laid_butter_z - wooden_tray_z
    # ketchup_height = laid_ketchup_z - wooden_tray_z
    # tomato_sauce_height = laid_tomato_sauce_z - wooden_tray_z
    # tolerance = 0.005
    # butter_min_z = butter_height - tolerance
    # butter_max_z = butter_height + tolerance
    # ketchup_min_z = ketchup_height - tolerance
    # ketchup_max_z = ketchup_height + tolerance
    # tomato_sauce_min_z = tomato_sauce_height - tolerance
    # tomato_sauce_max_z = tomato_sauce_height + tolerance
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["alphabet_soup_1", "cream_cheese_1", "tomato_sauce_1", "ketchup_1", "butter_1", "wooden_tray_1"],
        goal_states=[
            ("RelaxedOn", "alphabet_soup_1", "wooden_tray_1"),
            ("RelaxedOn", "cream_cheese_1", "wooden_tray_1"),
            ("RelaxedOn", "tomato_sauce_1", "wooden_tray_1"),
            ("RelaxedOn", "ketchup_1", "wooden_tray_1"),
            ("RelaxedOn", "butter_1", "wooden_tray_1"),
            ("PositionWithinObject", "alphabet_soup_1", "wooden_tray_1", -0.1, -0.1, 0.035801, 0.1, 0.1, 0.045801),
            ("PositionWithinObject", "tomato_sauce_1", "wooden_tray_1", -0.1, -0.1, 0.035801, 0.1, 0.1, 0.045801),
            ("PositionWithinObject", "butter_1", "wooden_tray_1", -0.1, -0.1, 0.010438, 0.1, 0.1, 0.020438),
            ("PositionWithinObject", "cream_cheese_1", "wooden_tray_1", -0.1, -0.1, 0.010438, 0.1, 0.1, 0.020438),
            ("PositionWithinObject", "ketchup_1", "wooden_tray_1", -0.1, -0.1, 0.02153011, 0.1, 0.1, 0.03153011),
            ("AxisAlignedWithinWorldAxis", "alphabet_soup_1", "y", 85, 95, "z"),
            ("AxisAlignedWithinWorldAxis", "tomato_sauce_1", "y", 85, 95, "z"),
            ("Or", ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "z", 0, 5, "z"), ("AxisAlignedWithinWorldAxis", "cream_cheese_1", "z", 175, 180, "z")),
            ("Or", ("AxisAlignedWithinWorldAxis", "butter_1", "z", 0, 5, "z"), ("AxisAlignedWithinWorldAxis", "butter_1", "z", 175, 180, "z")),
            ("Or", ("AxisAlignedWithinWorldAxis", "ketchup_1", "z", 0, 5, "z"), ("AxisAlignedWithinWorldAxis", "ketchup_1", "z", 175, 180, "z")),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
