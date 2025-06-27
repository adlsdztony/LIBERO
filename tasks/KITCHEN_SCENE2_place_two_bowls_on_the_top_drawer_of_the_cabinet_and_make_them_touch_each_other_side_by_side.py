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
import itertools

def main():
    # kitchen_scene_2
    scene_name = "kitchen_scene2"
    language = "Place two bowls on the top drawer of the cabinet and make them touch each other side by side"

    objects_of_interest = ["wooden_cabinet_1", "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"]
    
    goal_states = [
        (
            "Any",
            (
                ("And",
                 ("And",
                    ("In", "akita_black_bowl_1", "wooden_cabinet_1_top_region"),
                    ("In", "akita_black_bowl_2", "wooden_cabinet_1_top_region"),
                 ),
                    ("InContact", "akita_black_bowl_1", "akita_black_bowl_2"),
                ),
                ("And",
                 ("And",
                    ("In", "akita_black_bowl_1", "wooden_cabinet_1_top_region"),
                    ("In", "akita_black_bowl_3", "wooden_cabinet_1_top_region"),
                 ), 
                    ("InContact", "akita_black_bowl_1", "akita_black_bowl_3"),
                ),
                ("And",
                 ("And",
                    ("In", "akita_black_bowl_2", "wooden_cabinet_1_top_region"),
                    ("In", "akita_black_bowl_3", "wooden_cabinet_1_top_region"),
                 ),
                    ("InContact", "akita_black_bowl_2", "akita_black_bowl_3"),
                )
            )
        ),
        ("Upright", "akita_black_bowl_1"),
        ("Upright", "akita_black_bowl_2"),
        ("Upright", "akita_black_bowl_3"),
    ]
    

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=objects_of_interest,
        goal_states=goal_states
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
