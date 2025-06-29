"""This is a standalone file for create a task in libero."""
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

    scene_name = "living_room_scene1"
    language = "Use the tomato sauce to push the alphabet soup to torch the basket and the gripper should not touch alphabet soup directly"
    # print(scene_name.upper() + '_' + '_'.join(language.lower().split()) + '.py')
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["alphabet_soup_1", "tomato_sauce_1", "basket_1"],
        goal_states=[
            ("ConstraintNever", ("InContact", "gripper0_finger1", "alphabet_soup_1")),
            ("ConstraintNever", ("InContact", "gripper0_finger2", "alphabet_soup_1")),
            ("ConstraintNever", ("InContact", "gripper0_finger1_pad", "alphabet_soup_1")),
            ("ConstraintNever", ("InContact", "gripper0_finger2_pad", "alphabet_soup_1")),
            ("Sequential", (
                ("InContact", "tomato_sauce_1", "alphabet_soup_1"),
                ("InContact", "alphabet_soup_1", "basket_1"),
            ))
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
