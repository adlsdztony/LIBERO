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
    language = "Arrange objects in a perfect line with plates at the ends and all three mugs standing upright in between, ordered left to right as porcelain mug, red coffee mug, and white yellow mug"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "porcelain_mug_1", "red_coffee_mug_1", "white_yellow_mug_1", "plate_2"],
        goal_states=[
            ("Or",
             ("All", (
                ("Linear", "plate_1", "porcelain_mug_1", "red_coffee_mug_1", 0.005),
                ("Linear", "porcelain_mug_1", "red_coffee_mug_1", "white_yellow_mug_1", 0.005),
                ("Linear", "red_coffee_mug_1", "white_yellow_mug_1", "plate_2", 0.005),
                ("Ordering", "plate_1", "porcelain_mug_1", "red_coffee_mug_1"),
                ("Ordering", "porcelain_mug_1", "red_coffee_mug_1", "white_yellow_mug_1"),
                ("Ordering", "red_coffee_mug_1", "white_yellow_mug_1", "plate_2")
             )), 
             ("All", (
                ("Linear", "plate_2", "porcelain_mug_1", "red_coffee_mug_1", 0.005),
                ("Linear", "porcelain_mug_1", "red_coffee_mug_1", "white_yellow_mug_1", 0.005),
                ("Linear", "red_coffee_mug_1", "white_yellow_mug_1", "plate_1", 0.005),
                ("Ordering", "plate_2", "porcelain_mug_1", "red_coffee_mug_1"),
                ("Ordering", "porcelain_mug_1", "red_coffee_mug_1", "white_yellow_mug_1"),
                ("Ordering", "red_coffee_mug_1", "white_yellow_mug_1", "plate_1")
             ))
            ),
            ("Upright", "porcelain_mug_1"),
            ("Upright", "red_coffee_mug_1"),
            ("Upright", "white_yellow_mug_1"),
            ("PosiLessThan", "porcelain_mug_1", "z", 0.44),
            ("PosiLessThan", "red_coffee_mug_1", "z", 0.44),
            ("PosiLessThan", "white_yellow_mug_1", "z", 0.44),
            ("PosiLessThan", "plate_1", "z", 0.44),
            ("PosiLessThan", "plate_2", "z", 0.44),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
