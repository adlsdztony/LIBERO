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

from libero.libero.benchmark.mu_creation import KitchenScene2

def main():

    scene_name = "kitchen_scene2"
    language = "Stack two bowls off-center on the plate with the third bowl placed separately touching the plate from the side"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3", "plate_1"],
        goal_states=[
            ("Any",(
                ("All", (
                    ("RelaxedOn", "akita_black_bowl_1", "plate_1"),
                    ("Not", ("On", "akita_black_bowl_1", "plate_1")),
                    ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_1"),
                    ("InContact", "akita_black_bowl_3", "plate_1"),
                    ("PosiLessThan", "akita_black_bowl_3", "z", 0.9),
                )),
                ("All", (
                    ("RelaxedOn", "akita_black_bowl_1", "plate_1"),
                    ("Not", ("On", "akita_black_bowl_1", "plate_1")),
                    ("StackBowl", "akita_black_bowl_3", "akita_black_bowl_1"),
                    ("InContact", "akita_black_bowl_2", "plate_1"),
                    ("PosiLessThan", "akita_black_bowl_2", "z", 0.9),
                )),
                ("All", (
                    ("RelaxedOn", "akita_black_bowl_2", "plate_1"),
                    ("Not", ("On", "akita_black_bowl_2", "plate_1")),
                    ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2"),
                    ("InContact", "akita_black_bowl_3", "plate_1"),
                    ("PosiLessThan", "akita_black_bowl_3", "z", 0.9),
                )),
                ("All", (
                    ("RelaxedOn", "akita_black_bowl_2", "plate_1"),
                    ("Not", ("On", "akita_black_bowl_2", "plate_1")),
                    ("StackBowl", "akita_black_bowl_3", "akita_black_bowl_2"),
                    ("InContact", "akita_black_bowl_1", "plate_1"),
                    ("PosiLessThan", "akita_black_bowl_1", "z", 0.9),
                )),
                ("All", (
                    ("RelaxedOn", "akita_black_bowl_3", "plate_1"),
                    ("Not", ("On", "akita_black_bowl_3", "plate_1")),
                    ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3"),
                    ("InContact", "akita_black_bowl_1", "plate_1"),
                    ("PosiLessThan", "akita_black_bowl_1", "z", 0.9),
                )),
                ("All", (
                    ("RelaxedOn", "akita_black_bowl_3", "plate_1"),
                    ("Not", ("On", "akita_black_bowl_3", "plate_1")),
                    ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3"),
                    ("InContact", "akita_black_bowl_2", "plate_1"),
                    ("PosiLessThan", "akita_black_bowl_2", "z", 0.9),
                )),
            ))
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
