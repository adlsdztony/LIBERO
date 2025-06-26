from libero.libero.utils.task_generation_utils import (
    generate_bddl_from_task_info,
    register_task_info,
)
from libero.libero.benchmark.mu_creation import KitchenScene2


def main():
    scene_name = "kitchen_scene2"
    language = "Place the bowls at three corners of the cabinet's top surface with the plate in the center, and close all drawers"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
            "akita_black_bowl_1",
            "akita_black_bowl_2",
            "akita_black_bowl_3",
            "plate_1",
            "wooden_cabinet_1",
        ],
        goal_states=[
            ("On", "akita_black_bowl_1", "wooden_cabinet_1_top_side"),
            ("On", "akita_black_bowl_2", "wooden_cabinet_1_top_side"),
            ("On", "akita_black_bowl_3", "wooden_cabinet_1_top_side"),
            ("On", "plate_1", "wooden_cabinet_1_top_side"),
            (
                "PositionWithinObject",
                "plate_1",
                "wooden_cabinet_1",
                -0.05,
                -0.05,
                0.1,
                0.05,
                0.05,
                0.3,
            ),
            ("Close", "wooden_cabinet_1_top_region"),
            ("Close", "wooden_cabinet_1_middle_region"),
            ("Close", "wooden_cabinet_1_bottom_region"),
            (
                "Any",
                (
                    (
                        "RightAngle",
                        "akita_black_bowl_1",
                        "akita_black_bowl_2",
                        "akita_black_bowl_3",
                        10.0,
                    ),
                    (
                        "RightAngle",
                        "akita_black_bowl_2",
                        "akita_black_bowl_1",
                        "akita_black_bowl_3",
                        10.0,
                    ),
                    (
                        "RightAngle",
                        "akita_black_bowl_3",
                        "akita_black_bowl_1",
                        "akita_black_bowl_2",
                        10.0,
                    ),
                ),
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
