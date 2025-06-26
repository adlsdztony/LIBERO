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
    language = "Place the cream cheese block upside down touching the alphabet soup can which is lying with its side against the table"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["alphabet_soup_1", "cream_cheese_1"],
        goal_states=[
            ("UpsideDown", "cream_cheese_1"),
            ("InContact", "cream_cheese_1", "alphabet_soup_1"),
            # use (80, 100) rather than (85, 90) due to the rim of the cup lid and its pull tab
            ("AxisAlignedWithin", "alphabet_soup_1", "y", 80, 100),
            ("PosiLessThan", "alphabet_soup_1", "z", 0.474),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
