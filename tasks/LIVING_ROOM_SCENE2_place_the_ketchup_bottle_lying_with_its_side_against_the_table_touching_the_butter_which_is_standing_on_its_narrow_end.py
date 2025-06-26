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
    language = "Place the ketchup bottle lying with its side against the table touching the butter which is standing on its narrow end"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["alphabet_soup_1", "cream_cheese_1"],
        goal_states=[
            ("AxisAlignedWithin", "butter_1", "z", 85, 90),
            ("AxisAlignedWithin", "ketchup_1", "y", 85, 95),
            ("InContact", "ketchup_1", "butter_1"),
            ("PosiLessThan", "ketchup_1", "z", 0.464),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
