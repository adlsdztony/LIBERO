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

from libero.libero.benchmark.mu_creation import KitchenScene2






def main():
    scene_name = "kitchen_scene2"
    language = "Line three bowls up so that the distance in between increases from left to right"
    
    b1, b2, b3 = "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
        goal_states=[
            
            ("linear", b1, b2, b3, 0.01),
            ("ordering", b1, b2, b3),
            ("positionwithinobjectannulus", b2, b1, 0.0, 0.15), 
            ("positionwithinobjectannulus", b3, b2, 0.15, 0.40),
            # All three bowls are placed below the height of the table
            ("posilessthan", b1, "z", 0.90),
            ("posilessthan", b2, "z", 0.90),
            ("posilessthan", b3, "z", 0.90),  

            
            
            
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
