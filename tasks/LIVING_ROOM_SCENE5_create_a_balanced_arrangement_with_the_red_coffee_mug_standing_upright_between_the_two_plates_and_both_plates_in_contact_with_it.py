"""This is a standalone file for creating a task in libero."""
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

    # Write your reward code here
    scene_name = "living_room_scene5"
    language = "Create a balanced arrangement with the red coffee mug standing upright between the two plates and both plates in contact with it"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "red_coffee_mug_1", "plate_2"],
        goal_states=[
            ('RelaxedOn', 'plate_1', 'red_coffee_mug_1'), 
            ('RelaxedOn', 'plate_2', 'red_coffee_mug_1'), 
            ('RelaxedBetween', 'plate_1', 'red_coffee_mug_1', 'plate_2', 'y'),
            ("Upright", 'red_coffee_mug_1'),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
