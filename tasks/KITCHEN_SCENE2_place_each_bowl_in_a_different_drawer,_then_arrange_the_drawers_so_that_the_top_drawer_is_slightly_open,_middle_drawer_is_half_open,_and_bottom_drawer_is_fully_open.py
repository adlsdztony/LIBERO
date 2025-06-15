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

from libero.libero.benchmark.mu_creation import KitchenScene2

def main():

    scene_name = "kitchen_scene2"
    language = "Place each bowl in a different drawer, then arrange the drawers so that the top drawer is slightly open, middle drawer is half open, and bottom drawer is fully open"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3", "wooden_cabinet_1"],
        goal_states=[            
            ("Any", (
                ("And", ("In", "akita_black_bowl_1", "wooden_cabinet_1_top_region"), ("And", ("In", "akita_black_bowl_2", "wooden_cabinet_1_middle_region"), ("In", "akita_black_bowl_3", "wooden_cabinet_1_bottom_region"))),
                ("And", ("In", "akita_black_bowl_1", "wooden_cabinet_1_top_region"), ("And", ("In", "akita_black_bowl_3", "wooden_cabinet_1_middle_region"), ("In", "akita_black_bowl_2", "wooden_cabinet_1_bottom_region"))),
                ("And", ("In", "akita_black_bowl_2", "wooden_cabinet_1_top_region"), ("And", ("In", "akita_black_bowl_1", "wooden_cabinet_1_middle_region"), ("In", "akita_black_bowl_3", "wooden_cabinet_1_bottom_region"))),
                ("And", ("In", "akita_black_bowl_2", "wooden_cabinet_1_top_region"), ("And", ("In", "akita_black_bowl_3", "wooden_cabinet_1_middle_region"), ("In", "akita_black_bowl_1", "wooden_cabinet_1_bottom_region"))),
                ("And", ("In", "akita_black_bowl_3", "wooden_cabinet_1_top_region"), ("And", ("In", "akita_black_bowl_1", "wooden_cabinet_1_middle_region"), ("In", "akita_black_bowl_2", "wooden_cabinet_1_bottom_region"))),
                ("And", ("In", "akita_black_bowl_3", "wooden_cabinet_1_top_region"), ("And", ("In", "akita_black_bowl_2", "wooden_cabinet_1_middle_region"), ("In", "akita_black_bowl_1", "wooden_cabinet_1_bottom_region")))
            )),
            ("StairCase", "wooden_cabinet_1_top_region", "wooden_cabinet_1_middle_region", "wooden_cabinet_1_bottom_region"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
