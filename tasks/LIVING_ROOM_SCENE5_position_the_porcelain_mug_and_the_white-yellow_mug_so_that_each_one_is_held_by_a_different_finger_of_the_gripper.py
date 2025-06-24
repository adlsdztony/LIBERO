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
    language = "Position the porcelain mug and the white-yellow mug so that each one is held by a different finger of the gripper"
    case_A = (
    "all",
        (
            ("incontact", "porcelain_mug_1",     "gripper0_finger1_pad"),
            ("not", ("incontact", "porcelain_mug_1",     "gripper0_finger2_pad")),
            ("incontact", "white_yellow_mug_1",  "gripper0_finger2_pad"),
            ("not", ("incontact", "white_yellow_mug_1",  "gripper0_finger1_pad")),
        ),
    )

    case_B = (
        "all",
        (
            ("incontact", "porcelain_mug_1",     "gripper0_finger2_pad"),
            ("not", ("incontact", "porcelain_mug_1",     "gripper0_finger1_pad")),
            ("incontact", "white_yellow_mug_1",  "gripper0_finger1_pad"),
            ("not", ("incontact", "white_yellow_mug_1",  "gripper0_finger2_pad")),
        ),
    )

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1","white_yellow_mug_1"],
        goal_states=[
            
            ("or", case_A, case_B),
                
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()