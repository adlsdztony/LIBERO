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
    language = "Position the three bowls so their centers form a perfect right angle with one bowl at the corner"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
            "akita_black_bowl_1",
            "akita_black_bowl_2",
            "akita_black_bowl_3",
        ],
        goal_states=[
            # Main constraint: Three bowls must form a right angle
            # We use Any to allow any bowl to be at the corner
            (
                "Any",
                (
                    # Option 1: Bowl 1 at corner, Bowl 2 and Bowl 3 form the arms
                    (
                        "RightAngle",
                        "akita_black_bowl_1",
                        "akita_black_bowl_2",
                        "akita_black_bowl_3",
                        5.0,
                    ),
                    # Option 2: Bowl 2 at corner, Bowl 1 and Bowl 3 form the arms
                    (
                        "RightAngle",
                        "akita_black_bowl_2",
                        "akita_black_bowl_3",
                        "akita_black_bowl_1",
                        5.0,
                    ),
                    (
                        "RightAngle",
                        "akita_black_bowl_3",
                        "akita_black_bowl_1",
                        "akita_black_bowl_2",
                        5.0,
                    ),
                ),
            ),
            # Ensure bowls are at similar heights (prevent stacking)
            ("SameHeight", "akita_black_bowl_1", "akita_black_bowl_2"),
            ("SameHeight", "akita_black_bowl_2", "akita_black_bowl_3"),
            ("SameHeight", "akita_black_bowl_1", "akita_black_bowl_3"),
            # Prevent reward hacking: bowls should not be stacked on each other
            ("Not", ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2")),
            ("Not", ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3")),
            ("Not", ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3")),
            # Ensure the arrangement is not collinear (prevent degenerate cases)
            (
                "Not",
                (
                    "Linear",
                    "akita_black_bowl_1",
                    "akita_black_bowl_2",
                    "akita_black_bowl_3",
                    0.01,
                ),
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
