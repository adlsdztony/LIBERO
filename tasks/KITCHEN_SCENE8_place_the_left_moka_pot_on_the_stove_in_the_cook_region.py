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

from libero.libero.benchmark.mu_creation import KitchenScene8

def main():
    scene_name = "kitchen_scene8"
    language = "Place the left moka pot on the stove in the cook region"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["moka_pot_2","flat_stove_1"],
        goal_states=[
            ("upright","moka_pot_2"),
            ("on", "moka_pot_2", "flat_stove_1_cook_region"),
    
            
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()