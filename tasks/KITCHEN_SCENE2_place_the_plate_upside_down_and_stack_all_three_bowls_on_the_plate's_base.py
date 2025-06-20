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
    language = "Place the plate upside down and stack all three bowls on the plate's base"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
        goal_states=[
            ("Any", (
                ("All", (
                    ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2"),
                    ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3"),
                    )),
                ("All", (
                    ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3"),
                    ("StackBowl", "akita_black_bowl_3", "akita_black_bowl_2"),
                    )),
                ("All", (
                    ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_1"),
                    ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3"),
                    )),
                ),
            ),
            ("UpsideDown", "plate_1"),
            ("Upright", "akita_black_bowl_1"),
            ("Upright", "akita_black_bowl_2"),
            ("Upright", "akita_black_bowl_3"),

            ("Any", (
                ("RelaxedOn", "akita_black_bowl_1", "plate_1"),
                ("RelaxedOn", "akita_black_bowl_2", "plate_1"),
                ("RelaxedOn", "akita_black_bowl_3", "plate_1"),
            )),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
