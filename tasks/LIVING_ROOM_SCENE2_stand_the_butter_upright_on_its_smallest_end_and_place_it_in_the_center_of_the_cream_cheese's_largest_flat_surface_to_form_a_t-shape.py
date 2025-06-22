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
    language = "Stand the butter upright on its smallest end and place it in the center of the cream cheese's largest flat surface to form a upside down T-shape"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1", "cream_cheese_1"],
        goal_states=[
            ("AxisAlignedWithin", "butter_1", "z", 85, 95),
            ("FlexibleOn", "butter_1", "cream_cheese_1", 0.01, 0.01),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
