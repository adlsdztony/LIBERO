import numpy as np

from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)

from libero.libero.benchmark.mu_creation import *

# ============================================================
# Helper constants
SCENE_NAME = "kitchen_scene2"
B1, B2, B3 = "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"
PLATE = "plate_1"
# ============================================================


def register_nested_touch_task():
    """Task 2 - Two bowls nested, third touches the nested pair."""
    language = "Place two bowls nested inside each other with the third bowl positioned to touch the nested pair"

    cfg1in2_touch3 = (
        "And",
        ("StackBowl", B1, B2),
        ("Or", ("InContact", B3, B1), ("InContact", B3, B2)),
    )
    cfg1in3_touch2 = (
        "And",
        ("StackBowl", B1, B3),
        ("Or", ("InContact", B2, B1), ("InContact", B2, B3)),
    )
    cfg2in3_touch1 = (
        "And",
        ("StackBowl", B2, B3),
        ("Or", ("InContact", B1, B2), ("InContact", B1, B3)),
    )

    goal_states = [
        (
            "Any",
            (
                cfg1in2_touch3,
                cfg1in3_touch2,
                cfg2in3_touch1,
            ),
        )
    ]

    register_task_info(
        language,
        scene_name=SCENE_NAME,
        objects_of_interest=[B1, B2, B3],
        goal_states=goal_states,
    )

    bddl, _ = generate_bddl_from_task_info()
    print(bddl)


# ============================================================
# Main entry point
# ============================================================


def main():
    register_nested_touch_task()

    bddl_files, failures = generate_bddl_from_task_info()
    print("Generated BDDL:", bddl_files)
    if failures:
        print("Failures during generation:", failures)


if __name__ == "__main__":
    main()
