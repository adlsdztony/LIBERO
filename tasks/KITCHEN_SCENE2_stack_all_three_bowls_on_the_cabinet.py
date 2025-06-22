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
    # kitchen_scene_2
    scene_name = "kitchen_scene2"
    language = "Stack all three bowls on the cabinet"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_cabinet_1", "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
        goal_states=[
            (
                "Any",
                (
                    ("InContact", "wooden_cabinet_1", "akita_black_bowl_1"),
                    ("InContact", "wooden_cabinet_1", "akita_black_bowl_2"),
                    ("InContact", "wooden_cabinet_1", "akita_black_bowl_3"),
                )
            ),
            ("Or", ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2"), ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3")),
            ("Or", ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3"), ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_1")),
            ("Or", ("StackBowl", "akita_black_bowl_3", "akita_black_bowl_1"), ("StackBowl", "akita_black_bowl_3", "akita_black_bowl_2")),
            (
                "Any",
                (
                    ("RelaxedOn", "akita_black_bowl_1", "wooden_cabinet_1"),
                    ("RelaxedOn", "akita_black_bowl_2", "wooden_cabinet_1"),
                    ("RelaxedOn", "akita_black_bowl_3", "wooden_cabinet_1"),
                )
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
