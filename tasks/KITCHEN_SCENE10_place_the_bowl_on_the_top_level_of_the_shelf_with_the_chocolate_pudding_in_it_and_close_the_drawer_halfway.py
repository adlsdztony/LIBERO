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

from libero.libero.benchmark.mu_creation import KitchenScene10

def main():
    scene_name = "kitchen_scene10"
    language = "Place the bowl on the top level of the shelf with the chocolate pudding in it and close the drawer halfway"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1","chocolate_pudding_1","wooden_cabinet_1"],
        goal_states=[
            ("in",          "akita_black_bowl_1", "wooden_cabinet_1_top_region"),
            ("upright",     "akita_black_bowl_1"),
            ("relaxedon",   "chocolate_pudding_1","akita_black_bowl_1"),
            ("openratio",   "wooden_cabinet_1_top_region", 0.5),    
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()