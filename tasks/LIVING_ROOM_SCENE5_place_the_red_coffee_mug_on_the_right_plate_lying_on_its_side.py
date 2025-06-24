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
    language = "Place the red coffee mug on the right plate lying on its side"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[ "red_coffee_mug_1","plate_2"],
        goal_states=[
            ("on", "red_coffee_mug_1", "plate_2"),
            ("not", ("upright", "red_coffee_mug_1")),
            ("not", ("upsidedown", "red_coffee_mug_1")),
            ("axisalignedwithin", "red_coffee_mug_1", "z", 60.0, 120.0),
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()