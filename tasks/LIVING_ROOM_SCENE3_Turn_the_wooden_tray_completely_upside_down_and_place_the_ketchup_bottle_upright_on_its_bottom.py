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
    language = "Turn wooden tray upside down and place ketchup bottle upright on its bottom"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1","wooden_tray_1"],
        goal_states=[
            ("InContact", "ketchup_1", "wooden_tray_1"),
            ("UpsideDown", "wooden_tray_1"),
            ("Under", "wooden_tray_1", "ketchup_1"),
            ("AxisAlignedWithin", "ketchup_1", "y", 0, 5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()