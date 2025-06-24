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

from libero.libero.benchmark.mu_creation import StudyScene3

def main():
    scene_name = "study_scene3"
    language = "Put both mugs into the compartments of the desk caddy"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1","black_book_1"],
        goal_states=[
            "or",
            ("and",
            ("In", "porcelain_mug_1", "desk_caddy_1_left_contain_region"),
            ("In", "red_coffee_mug_1", "desk_caddy_1_right_contain_region"),
            ),    
            ("and",
            ("In","red_coffee_mug_1",  "desk_caddy_1_left_contain_region"),
            ("In", "porcelain_mug_1", "desk_caddy_1_right_contain_region"),
            )        
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()