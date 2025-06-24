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

from libero.libero.benchmark.mu_creation import LivingRoomScene5

def main():
    scene_name = "living_room_scene5"
    language = "Rotate the white-yellow and porcelain mugs so that their handles aligned in the same direction"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1","white_yellow_mug_1"],
        goal_states=[
            
            ("yawanglealigned",
                "white_yellow_mug_1",      
                "porcelain_mug_1",         
                15.0,                  
                180.0),                     
            
                
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()