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

    scene_name = "kitchen_scene10"
    language = "Place one butter pack inside the drawer while keeping the other butter pack on top of the chocolate pudding"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chocolate_pudding_1", "butter_1", "butter_2", "wooden_cabinet_1"],
        goal_states=[
            ("Or",
                ("And",
                    ("Any",
                        (("In", "butter_1", "wooden_cabinet_1_top_region"),
                        ("In", "butter_1", "wooden_cabinet_1_middle_region"),
                        ("In", "butter_1", "wooden_cabinet_1_bottom_region"))
                    ),
                    ("On", "butter_2", "chocolate_pudding_1")
                ),
                ("And",
                    ("Any",
                        (("In", "butter_2", "wooden_cabinet_1_top_region"),
                        ("In", "butter_2", "wooden_cabinet_1_middle_region"),
                        ("In", "butter_2", "wooden_cabinet_1_bottom_region"))
                    ),
                    ("On", "butter_1", "chocolate_pudding_1")
                )
            )
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
