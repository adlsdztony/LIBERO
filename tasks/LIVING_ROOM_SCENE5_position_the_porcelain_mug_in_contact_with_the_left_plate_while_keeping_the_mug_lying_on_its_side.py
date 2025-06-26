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

from libero.libero.benchmark.mu_creation import LivingRoomScene5


def main():
    # living_room_scene_5
    scene_name = "living_room_scene5"
    language = "Position the porcelain mug in contact with the left plate while keeping the mug lying on its side"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "plate_2"],
        goal_states=[
            ('InContact', 'porcelain_mug_1', 'plate_2'), 
            ("AxisAlignedWithin", "porcelain_mug_1", "z", "85", "95"),
        ],
    )


    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
