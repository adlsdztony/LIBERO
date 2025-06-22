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


def main():
    """Task 3 - Bowls form contact triangle, plate touches exactly one bowl."""
    language = "Position all three bowls so each touches the other two, with the plate touching one bowl"

    triangle_contacts = (
        "All",
        (
            ("InContact", B1, B2),
            ("InContact", B1, B3),
            ("InContact", B2, B3),
        ),
    )

    plate_touch_1 = (
        "All",
        (
            ("InContact", PLATE, B1),
            ("Not", ("InContact", PLATE, B2)),
            ("Not", ("InContact", PLATE, B3)),
        ),
    )
    plate_touch_2 = (
        "All",
        (
            ("InContact", PLATE, B2),
            ("Not", ("InContact", PLATE, B1)),
            ("Not", ("InContact", PLATE, B3)),
        ),
    )
    plate_touch_3 = (
        "All",
        (
            ("InContact", PLATE, B3),
            ("Not", ("InContact", PLATE, B1)),
            ("Not", ("InContact", PLATE, B2)),
        ),
    )

    goal_states = [
        triangle_contacts,
        ("Any", (plate_touch_1, plate_touch_2, plate_touch_3)),
        # Anti-stacking
        ("SameHeight", B1, B2),
        ("SameHeight", B2, B3),
        ("Not", ("StackBowl", B1, B2)),
        ("Not", ("StackBowl", B1, B3)),
        ("Not", ("StackBowl", B2, B3)),
    ]

    register_task_info(
        language,
        scene_name=SCENE_NAME,
        objects_of_interest=[PLATE, B1, B2, B3],
        goal_states=goal_states,
    )

    bddl, _ = generate_bddl_from_task_info()
    print(bddl)

if __name__ == "__main__":
    main()