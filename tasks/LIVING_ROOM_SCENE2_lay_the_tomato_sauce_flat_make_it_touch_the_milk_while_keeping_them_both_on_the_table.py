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
    scene_name = "living_room_scene2"
    language = "Lay the tomato sauce flat make it touch the milk while keeping them both on the table"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1","tomato_sauce_1"],
        goal_states=[
            ("InContact", "tomato_sauce_1", "milk_1"),
            ("PositionWithin", "milk_1", 0, 0, 0.48, 1.0, 1.0, 0.04),  # milk is on the table
            ("PosiLessThan", "tomato_sauce_1", "z", 0.474),  # tomato sauce is laid on the table (upright height is 0.475)
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()