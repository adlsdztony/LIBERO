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
    language = "Create a stepped arrangement with one bowl on the table, another bowl on the middle drawer, and the third bowl on top of the cabinet"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
        goal_states=[
            ("Any", (
                ("All", (
                    ("PositionWithin", "akita_black_bowl_1", -0.004, 0, 0.898, 0.05, 1, 0.01), # on table
                    ("In", "akita_black_bowl_2", "wooden_cabinet_1_middle_region"), # on middle drawer
                    ("On", "akita_black_bowl_3", "wooden_cabinet_1_top_side"), # on top of the cabinet
                )),
                ("All", (
                    ("PositionWithin", "akita_black_bowl_1", -0.004, 0, 0.898, 0.05, 1, 0.01),
                    ("In", "akita_black_bowl_3", "wooden_cabinet_1_middle_region"),
                    ("On", "akita_black_bowl_2", "wooden_cabinet_1_top_side"),
                )),
                ("All", (
                    ("PositionWithin", "akita_black_bowl_2", -0.004, 0, 0.898, 0.05, 1, 0.01),
                    ("In", "akita_black_bowl_1", "wooden_cabinet_1_middle_region"),
                    ("On", "akita_black_bowl_3", "wooden_cabinet_1_top_side"),
                )),
                ("All", (
                    ("PositionWithin", "akita_black_bowl_2", -0.004, 0, 0.898, 0.05, 1, 0.01),
                    ("In", "akita_black_bowl_3", "wooden_cabinet_1_middle_region"),
                    ("On", "akita_black_bowl_1", "wooden_cabinet_1_top_side"),
                )),
                ("All", (
                    ("PositionWithin", "akita_black_bowl_3", -0.004, 0, 0.898, 0.05, 1, 0.01),
                    ("In", "akita_black_bowl_1", "wooden_cabinet_1_middle_region"),
                    ("On", "akita_black_bowl_2", "wooden_cabinet_1_top_side"),
                )),
                ("All", (
                    ("PositionWithin", "akita_black_bowl_3", -0.004, 0, 0.898, 0.05, 1, 0.01),
                    ("In", "akita_black_bowl_2", "wooden_cabinet_1_middle_region"),
                    ("On", "akita_black_bowl_1", "wooden_cabinet_1_top_side"),
                )),
            )),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()