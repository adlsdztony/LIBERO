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

from libero.libero.benchmark.mu_creation import LivingRoomScene2

def main():

    scene_name = "living_room_scene2"
    language = "Arrange the butter, cream cheese, milk, and orange juice so that the planar distance between each item increases in this order"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1", "butter_1", "cream_cheese_1", "orange_juice_1"],
        goal_states=[
            ("GreaterThan", ("PlanarDistance", "cream_cheese_1", "milk_1"), ("PlanarDistance", "butter_1", "cream_cheese_1")),
            ("GreaterThan", ("PlanarDistance", "orange_juice_1", "milk_1"), ("PlanarDistance", "milk_1", "cream_cheese_1")),
            ("PosiLessThan", "milk_1", "z", 0.51),
            ("PosiLessThan", "butter_1", "z", 0.45),
            ("PosiLessThan", "cream_cheese_1", "z", 0.45),
            ("PosiLessThan", "orange_juice_1", "z", 0.51),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
