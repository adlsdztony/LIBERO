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
    language = "Create a nested mug arrangement with red coffee inside white-yellow inside porcelain mug, all upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "white_yellow_mug_1", "red_coffee_mug_1"],
        goal_states=[
            ("RelaxedOn", "red_coffee_mug_1", "white_yellow_mug_1"),
            ("RelaxedOn", "white_yellow_mug_1", "porcelain_mug_1"),
            ("Upright", "porcelain_mug_1"),
            ("Upright", "white_yellow_mug_1"),
            ("Upright", "red_coffee_mug_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
