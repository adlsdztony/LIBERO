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

from libero.libero.benchmark.mu_creation import LivingRoomScene5

def main():
    scene_name = "living_room_scene5"
    language = "Position the white-yellow mug lying sideways on the left plate"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[ "white_yellow_mug_1","plate_1"],
        goal_states=[
            ("on", "white_yellow_mug_1", "plate_1"),
            ("not", ("upright", "white_yellow_mug_1")),
            ("not", ("upsidedown", "white_yellow_mug_1")),
            ("axisalignedwithin", "white_yellow_mug_1", "z", 60.0, 120.0),
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()