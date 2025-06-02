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
    # living_room_scene6
    scene_name = "living_room_scene6"
    language = "Place the porcelain mug upsidedown on the center of plate"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1","plate_1"],
        goal_states=[
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 175, 180 ),
            ("On", "porcelain_mug_1", "plate_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()