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
    language = "Stand the ketchup and cream cheese upright on the table, touching each other, and position them right next to the basket so that at least one of them touches its outer side"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "cream_cheese_1", "basket_1"],
        goal_states=[
            ("AxisAlignedWithin", "ketchup_1", "y", 0, 5),
            ("AxisAlignedWithin", "cream_cheese_1", "z", 85, 95),
            ("InContact", "ketchup_1", "cream_cheese_1"),
            ("InContact", "cream_cheese_1", "basket_1"),
            ("Equal", ("GetPosi", "ketchup_1", "z"), 0.509, 0.001),
            ("Equal", ("GetPosi", "cream_cheese_1", "z"), 0.445, 0.001),
            ("Equal", ("GetPosi", "basket_1", "z"), 0.432, 0.001),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
