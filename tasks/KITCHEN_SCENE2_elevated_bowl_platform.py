from libero.libero.utils.task_generation_utils import (
    generate_bddl_from_task_info,
    register_task_info,
)
from libero.libero.benchmark.mu_creation import KitchenScene2


def order(x, y, z):
    return (
        "And",
        (
            "And",
            (
                "And",
                ("Upright", f"akita_black_bowl_{x}"),
                ("Upright", f"akita_black_bowl_{y}"),
            ),
            (
                "And",
                ("RelaxedOn", f"plate_1", f"akita_black_bowl_{x}"),
                ("RelaxedOn", f"plate_1", f"akita_black_bowl_{y}"),
            ),
        ),
        (
            "And",
            (
                "And",
                (
                    "Not",
                    ("InContact", f"akita_black_bowl_{x}", f"akita_black_bowl_{y}"),
                ),
                ("Upright", f"akita_black_bowl_{z}"),
            ),
            ("RelaxedOn", f"akita_black_bowl_{z}", f"plate_1"),
        ),
    )


def main():
    scene_name = "kitchen_scene2"
    language = "Place two bowls upright side by side, put the plate on top of them as a platform, then place the third bowl upright on the plate"
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
                    order(2, 3, 1),
                    order(3, 1, 2),
                ),
            )
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
