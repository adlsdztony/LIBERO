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
    # living_room_scene3
    scene_name = "living_room_scene3"
    language = "Place the ketchup in the center of wooden tray, then lift the tray up along with its contents, making sure it doesn't touch the tabletop"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1","wooden_tray_1"],
        goal_states=[
            ("PosiGreaterThan", "wooden_tray_1", "z", 0.55),
            ("RelaxedOn", "ketchup_1", "wooden_tray_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()