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
    language = (
        "Place the plate standing vertically with one bowl touching it on each side"
    )
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
            "plate_1",
            "akita_black_bowl_1",
            "akita_black_bowl_2",
            "akita_black_bowl_3",
        ],
        goal_states=[
            # Plate must be standing vertically
            ("AxisAlignedWithin", "plate_1", "z", 80, 100),
            # Two bowls must be touching the plate on opposite sides
            # Allow any two of the three bowls to be used
            (
                "Any",
                (
                    # Option 1: Bowl 1 and Bowl 2
                    (
                        "And",
                        (
                            "And",
                            ("InContact", "akita_black_bowl_1", "plate_1"),
                            ("InContact", "akita_black_bowl_2", "plate_1"),
                        ),
                        (
                            "OppositeSides",
                            "akita_black_bowl_1",
                            "akita_black_bowl_2",
                            "plate_1",
                        ),
                    ),
                    # Option 2: Bowl 1 and Bowl 3
                    (
                        "And",
                        (
                            "And",
                            ("InContact", "akita_black_bowl_1", "plate_1"),
                            ("InContact", "akita_black_bowl_3", "plate_1"),
                        ),
                        (
                            "OppositeSides",
                            "akita_black_bowl_1",
                            "akita_black_bowl_3",
                            "plate_1",
                        ),
                    ),
                    # Third option
                    (
                        "And",
                        (
                            "And",
                            ("InContact", "akita_black_bowl_2", "plate_1"),
                            ("InContact", "akita_black_bowl_3", "plate_1"),
                        ),
                        (
                            "OppositeSides",
                            "akita_black_bowl_2",
                            "akita_black_bowl_3",
                            "plate_1",
                        ),
                    ),
                ),
            ),
            # Prevent reward hacking: bowls should not be stacked
            ("Not", ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2")),
            ("Not", ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3")),
            ("Not", ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3")),
            # Prevent bowls from being placed on top of plate
            ("Not", ("RelaxedOn", "akita_black_bowl_1", "plate_1")),
            ("Not", ("RelaxedOn", "akita_black_bowl_2", "plate_1")),
            ("Not", ("RelaxedOn", "akita_black_bowl_3", "plate_1")),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
