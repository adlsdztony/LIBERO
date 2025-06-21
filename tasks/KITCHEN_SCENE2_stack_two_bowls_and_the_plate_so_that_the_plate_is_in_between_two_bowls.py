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
    language = "Stack two bowls and the plate so that the plate is in between two bowls"
    
    
    plate = "plate_1"
    bowls = ["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"]

    def stack_variant(bottom, top):
        return (
            "and",
            ("and",
            ("relaxedon", plate, bottom),      
            ("relaxedon", top, plate),
            ),
            ("and",         
            ("stackbowl", bottom, plate),       
            ("stackbowl", plate,  top),
            ),
        )
    
    variant_expr = ("or",
                    stack_variant(bowls[0], bowls[1]),
                    ("or",
                     stack_variant(bowls[0], bowls[2]),
                     ("or",
                      stack_variant(bowls[1], bowls[0]),
                      ("or",
                       stack_variant(bowls[1], bowls[2]),
                       ("or",
                        stack_variant(bowls[2], bowls[0]),
                        stack_variant(bowls[2], bowls[1]),
                       ),
                      ),
                     ),
                    )
                   )

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3", "plate_1"],
        goal_states=[
            
            variant_expr,
            ("upright", plate),
            ("upright", "akita_black_bowl_1"),
            ("upright", "akita_black_bowl_2"),
            ("upright", "akita_black_bowl_3"),   

            
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
