# stack_two_bowls_and_place_the_plate_on_top_of_them
# make_the_three_bowls_touch_each_other
# make_the_three_bowls_touch_each_other_and_the_plate_on_top_of_them

# Stack two bowls and place the plate on top of them
# Make the three bowls touch each other
# Make the three bowls touch each other and the plate on top of them

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

    scene_name = "kitchen_scene2"
    language = "Make the three bowls touch each other"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
        goal_states=[
            ("InContact", "akita_black_bowl_1", "akita_black_bowl_2"),
            ("InContact", "akita_black_bowl_1", "akita_black_bowl_3"),
            ("InContact", "akita_black_bowl_2", "akita_black_bowl_3"),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
