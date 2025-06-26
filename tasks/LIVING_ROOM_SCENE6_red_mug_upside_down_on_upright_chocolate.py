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

from libero.libero.benchmark.mu_creation import *

def main():

    scene_name = "living_room_scene6"
    language = "position the red coffee mug upside down on the chocolate pudding while keeping the pudding upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["red_coffee_mug_1", "chocolate_pudding_1", "porcelain_mug_1", "plate_1"],
        goal_states=[
            ("RelaxedOn", "red_coffee_mug_1", "chocolate_pudding_1"),
            ("UpsideDown", "red_coffee_mug_1"),
            ("Upright", "chocolate_pudding_1"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main() 