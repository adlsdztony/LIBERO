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
    language = "Stack one cheese rotating 90 degrees horizontally on another one"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1","butter_2"],
        goal_states=[
            "or",
       
        (   "and",
            
            ("and",
            ("on",        "butter_2", "butter_1"),          
            ("upright",   "butter_1"),),
            ("and",
            ("upright",   "butter_2"),
            ("orientedatdegree",
                "butter_2",
                0.0, 0.0, 90,                
                180, 180, 10),)
        ),
       
        (   "and",
            ("and",
            ("on",        "butter_1", "butter_2"),          
            ("upright",   "butter_1"),),
            ("and",
            ("upright",   "butter_2"),
            ("orientedatdegree",
                "butter_1",
                0.0, 0.0, 90,
                180, 180, 10),)
        ),
    
            
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()