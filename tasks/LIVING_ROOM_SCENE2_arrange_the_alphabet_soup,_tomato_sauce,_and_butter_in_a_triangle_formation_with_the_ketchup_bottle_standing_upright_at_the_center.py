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

from libero.libero.benchmark.mu_creation import LivingRoomScene2

def main():

    scene_name = "living_room_scene2"
    language = "Arrange the alphabet soup, tomato sauce, and butter in a triangle formation with the ketchup bottle standing upright at the center"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "alphabet_soup_1", "tomato_sauce_1", "butter_1"],
        goal_states=[
            ("AxisAlignedWithin", "ketchup_1", "y", 0, 5),
            ("Not", ("Linear", "tomato_sauce_1", "alphabet_soup_1", "butter_1", 0.01)),
            ("Equal", ("GetPosi", "ketchup_1", "z"), 0.509, 0.001),
            ("Equal", ("GetPosi", "alphabet_soup_1", "z"), 0.475, 0.001),
            ("Equal", ("GetPosi", "butter_1", "z"), 0.445, 0.001),
            ("Equal", ("GetPosi", "tomato_sauce_1", "z"), 0.475, 0.001),
            ("Equal", ("GetPosi", "ketchup_1", "x"), 
                ("Arithmetic",
                    ("Arithmetic",
                        ("Arithmetic",
                            ("GetPosi", "alphabet_soup_1", "x"),
                            "add",
                            ("GetPosi", "tomato_sauce_1", "x"),
                        ),
                        "add",
                        ("GetPosi", "butter_1", "x"),
                    ),
                    "divide",
                    3.0
                ),
                0.03
            ),
            ("Equal", ("GetPosi", "ketchup_1", "y"), 
                ("Arithmetic",
                    ("Arithmetic",
                        ("Arithmetic",
                            ("GetPosi", "alphabet_soup_1", "y"),
                            "add",
                            ("GetPosi", "tomato_sauce_1", "y"),
                        ),
                        "add",
                        ("GetPosi", "butter_1", "y"),
                    ),
                    "divide",
                    3.0
                ),
                0.03
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
