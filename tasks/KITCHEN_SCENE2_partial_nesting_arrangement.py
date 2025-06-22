from libero.libero.utils.task_generation_utils import (
    generate_bddl_from_task_info,
    register_task_info,
)
from libero.libero.benchmark.mu_creation import KitchenScene2


def main():
    scene_name = "kitchen_scene2"
    language = "Stack two bowls on the plate, and position the third bowl separately on the cabinet with the top drawer open"
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
            # Nested Or structure to handle all 6 stacking combinations
            ("Or", 
                ("Or",
                    # Bowls 1&2 stacked on plate, bowl 3 on cabinet - Option 1
                    ("And",
                        ("And",
                            ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2"),
                            ("On", "akita_black_bowl_1", "plate_1"),
                        ),
                        ("And",
                            ("On", "akita_black_bowl_2", "akita_black_bowl_1"),
                            ("On", "akita_black_bowl_3", "wooden_cabinet_1_top_side"),
                        ),
                    ),
                    # Bowls 1&2 stacked on plate, bowl 3 on cabinet - Option 2
                    ("And",
                        ("And",
                            ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_2"),
                            ("On", "akita_black_bowl_2", "plate_1"),
                        ),
                        ("And",
                            ("On", "akita_black_bowl_1", "akita_black_bowl_2"),
                            ("On", "akita_black_bowl_3", "wooden_cabinet_1_top_side"),
                        ),
                    ),
                ),
                ("Or",
                    ("Or",
                        # Bowls 1&3 stacked on plate, bowl 2 on cabinet - Option 1
                        ("And",
                            ("And",
                                ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3"),
                                ("On", "akita_black_bowl_1", "plate_1"),
                            ),
                            ("And",
                                ("On", "akita_black_bowl_3", "akita_black_bowl_1"),
                                ("On", "akita_black_bowl_2", "wooden_cabinet_1_top_side"),
                            ),
                        ),
                        # Bowls 1&3 stacked on plate, bowl 2 on cabinet - Option 2
                        ("And",
                            ("And",
                                ("StackBowl", "akita_black_bowl_1", "akita_black_bowl_3"),
                                ("On", "akita_black_bowl_3", "plate_1"),
                            ),
                            ("And",
                                ("On", "akita_black_bowl_1", "akita_black_bowl_3"),
                                ("On", "akita_black_bowl_2", "wooden_cabinet_1_top_side"),
                            ),
                        ),
                    ),
                    ("Or",
                        # Bowls 2&3 stacked on plate, bowl 1 on cabinet - Option 1
                        ("And",
                            ("And",
                                ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3"),
                                ("On", "akita_black_bowl_2", "plate_1"),
                            ),
                            ("And",
                                ("On", "akita_black_bowl_3", "akita_black_bowl_2"),
                                ("On", "akita_black_bowl_1", "wooden_cabinet_1_top_side"),
                            ),
                        ),
                        # Bowls 2&3 stacked on plate, bowl 1 on cabinet - Option 2
                        ("And",
                            ("And",
                                ("StackBowl", "akita_black_bowl_2", "akita_black_bowl_3"),
                                ("On", "akita_black_bowl_3", "plate_1"),
                            ),
                            ("And",
                                ("On", "akita_black_bowl_2", "akita_black_bowl_3"),
                                ("On", "akita_black_bowl_1", "wooden_cabinet_1_top_side"),
                            ),
                        ),
                    ),
                ),
            ),
            # Cabinet drawer states
            ("Open", "wooden_cabinet_1_top_region"),
            ("Close", "wooden_cabinet_1_middle_region"),
            ("Close", "wooden_cabinet_1_bottom_region"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
