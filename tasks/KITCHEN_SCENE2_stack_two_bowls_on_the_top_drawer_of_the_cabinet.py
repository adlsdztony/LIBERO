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
    # kitchen_scene_2
    scene_name = "kitchen_scene2"
    language = "Stack two bowls on the top drawer of the cabinet"
    drawer_obj  = "wooden_cabinet_1_top_region"
    bowls = ["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"]
    def stack_pair(bottom, top):
        return (
            "and",
            ("in", bottom, "wooden_cabinet_1_top_region"),
            (
                "and",
                ("relaxedon", top, bottom),
                ("stackbowl", bottom, top),  
            ),
        )
    #Enumerate 6 sequences and link with or
    cfg = ("or",
           stack_pair("akita_black_bowl_1", "akita_black_bowl_2"),
           ("or",
            stack_pair("akita_black_bowl_2", "akita_black_bowl_1"),
            ("or",
             stack_pair("akita_black_bowl_1", "akita_black_bowl_3"),
             ("or",
              stack_pair("akita_black_bowl_3", "akita_black_bowl_1"),
              ("or",
               stack_pair("akita_black_bowl_2", "akita_black_bowl_3"),
               stack_pair("akita_black_bowl_3", "akita_black_bowl_2"),
              ),
             ),
            ),
           )
          )
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3", "wooden_cabinet_1"],
        goal_states=[
            
            cfg,
            ("upright", "akita_black_bowl_1"),
            ("upright", "akita_black_bowl_2"),
            ("upright", "akita_black_bowl_3"),
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
