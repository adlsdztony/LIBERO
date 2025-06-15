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
    language = "Create a tower by placing the milk on the alphabet soup, and position the ketchup touching the base of this tower."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1", "alphabet_soup_1", "ketchup_1"],
        goal_states=[
            ("On", "milk_1", "alphabet_soup_1"),
            ("InContact", "ketchup_1", "alphabet_soup_1"),
            ("InAir", "alphabet_soup_1", 0.45),
            ("InAir", "ketchup_1", 0.45)
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()