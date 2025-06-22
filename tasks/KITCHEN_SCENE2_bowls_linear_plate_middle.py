from libero.libero.utils.task_generation_utils import (
    generate_bddl_from_task_info,
    register_task_info,
)
from libero.libero.benchmark.mu_creation import KitchenScene2


def order(x, y, z):
    """x, y, plate, z"""

    def bowl(i):
        return f"akita_black_bowl_{i}"

    state = [
        ("Ordering", bowl(x), bowl(y), "plate_1"),
        ("Ordering", bowl(y), "plate_1", bowl(z)),
        ("Linear", bowl(x), bowl(y), "plate_1", 0.005),
        ("Linear", bowl(y), "plate_1", bowl(z), 0.005),
    ]

    def nest_and(states):
        if len(states) == 1:
            return states[0]
        return ("And", states[0], nest_and(states[1:]))

    return nest_and(state)


def main():
    scene_name = "kitchen_scene2"
    language = "Arrange the bowls and plate in a straight line with the plate sandwiched between two bowls on one side and one bowl on the other"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
            "akita_black_bowl_1",
            "akita_black_bowl_2",
            "akita_black_bowl_3",
            "plate_1",
        ],
        goal_states=[
            (
                "Any",
                (
                    order(1, 2, 3),
                    order(1, 3, 2),
                    order(2, 1, 3),
                    order(2, 3, 1),
                    order(3, 1, 2),
                    order(3, 2, 1),
                ),
            )
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
