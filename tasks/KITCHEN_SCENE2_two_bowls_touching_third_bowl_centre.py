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


# ============================================================
# Helper constants
SCENE_NAME = "kitchen_scene2"
B1, B2, B3 = "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"
PLATE = "plate_1"
# ============================================================


def main():
    """Task 1 - Two bowls touching, third centered between without touching."""
    language = (
        "Place two bowls touching each other and the third bowl exactly centered "
        "between them without touching"
    )

    # Three symmetric configurations captured via Any
    cfg12_3 = (
        "All",
        (
            ("InContact", B1, B2),
            ("RelaxedBetween", B1, B3, B2, "x"),
            ("RelaxedBetween", B1, B3, B2, "y"),
            ("Not", ("InContact", B3, B1)),
            ("Not", ("InContact", B3, B2)),
        ),
    )
    cfg13_2 = (
        "All",
        (
            ("InContact", B1, B3),
            ("RelaxedBetween", B1, B2, B3, "x"),
            ("RelaxedBetween", B1, B2, B3, "y"),
            ("Not", ("InContact", B2, B1)),
            ("Not", ("InContact", B2, B3)),
        ),
    )
    cfg23_1 = (
        "All",
        (
            ("InContact", B2, B3),
            ("RelaxedBetween", B2, B1, B3, "x"),
            ("RelaxedBetween", B2, B1, B3, "y"),
            ("Not", ("InContact", B1, B2)),
            ("Not", ("InContact", B1, B3)),
        ),
    )

    goal_states = [
        ("Any", (cfg12_3, cfg13_2, cfg23_1)),
        # Anti-stacking / robustness
        ("Not", ("StackBowl", B1, B2)),
        ("Not", ("StackBowl", B1, B3)),
        ("Not", ("StackBowl", B2, B3)),
    ]

    register_task_info(
        language,
        scene_name=SCENE_NAME,
        objects_of_interest=[B1, B2, B3],
        goal_states=goal_states,
    )

    bddl, _ = generate_bddl_from_task_info()
    print(bddl)


if __name__ == "__main__":
    main()
