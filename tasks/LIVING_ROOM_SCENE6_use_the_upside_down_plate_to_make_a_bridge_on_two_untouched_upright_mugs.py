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
    language = "use the upside down plate to make a bridge on two untouched upright mugs"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["red_coffee_mug_1", "porcelain_mug_1", "plate_1"],
        goal_states=[
            ("Upright", "red_coffee_mug_1"),
            ("Upright", "porcelain_mug_1"),
            ("PositionWithin", "porcelain_mug_1", 0.0, 0.0, 0.43436997, 1.0, 1.0, 0.005),
            ("PositionWithin", "red_coffee_mug_1", 0.0, 0.0, 0.43859901, 1.0, 1.0, 0.005),
            ("Not", ("InContact", "red_coffee_mug_1", "porcelain_mug_1")),
            ("UpsideDown", "plate_1"),
            ("RelaxedOn", "plate_1", "red_coffee_mug_1"),
            ("RelaxedOn", "plate_1", "porcelain_mug_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
