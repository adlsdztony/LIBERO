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

from libero.libero.benchmark.mu_creation import TabletopScene1

def main():
  
    scene_name = "tabletop_scene1"
    language = "Place the wine bottle on the plate and ensure it is upright"
    register_task_info(
        language=language,
        scene_name=scene_name,
        objects_of_interest=["wine_bottle_1", "plate_1"], 
        goal_states=[
            ("On", "wine_bottle_1", "main_table_plate_region"),  
            ("Upright", "wine_bottle_1"),
            ("InContact", "wine_bottle_1", "plate_1")                        
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()