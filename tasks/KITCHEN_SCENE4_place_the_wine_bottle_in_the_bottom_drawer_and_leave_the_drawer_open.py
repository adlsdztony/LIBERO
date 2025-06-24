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

from libero.libero.benchmark.mu_creation import KitchenScene4

def main():
    scene_name = "kitchen_scene4"
    language = "Place the wine bottle in the bottom drawer and leave the drawer open"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["white_cabinet_1", "wine_bottle_1"],
        goal_states=[
            ("in",   "wine_bottle_1", "white_cabinet_1_bottom_region"),   
            ("open", "white_cabinet_1_bottom_region"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()