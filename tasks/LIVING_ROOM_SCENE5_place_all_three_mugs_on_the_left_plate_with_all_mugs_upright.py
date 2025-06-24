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
    language = "Place all three mugs on the left plate with all mugs upright"



    # ------------------------------------------------------------------
    # 6 stacking orders, each consisting of three relaxedons, linked with "and"
    #    bottom on plate_1
    #    middle on bottom
    #    top    on middle
    # ------------------------------------------------------------------
    cfg1 = ("and",
            ("relaxedon", "porcelain_mug_1", "plate_1"),
            ("and",
             ("relaxedon", "red_coffee_mug_1", "porcelain_mug_1"),
             ("relaxedon", "white_yellow_mug_1", "red_coffee_mug_1"),
            ),
           )

    cfg2 = ("and",
            ("relaxedon", "porcelain_mug_1", "plate_1"),
            ("and",
             ("relaxedon", "white_yellow_mug_1", "porcelain_mug_1"),
             ("relaxedon", "red_coffee_mug_1", "white_yellow_mug_1"),
            ),
           )

    cfg3 = ("and",
            ("relaxedon", "red_coffee_mug_1", "plate_1"),
            ("and",
             ("relaxedon", "porcelain_mug_1", "red_coffee_mug_1"),
             ("relaxedon", "white_yellow_mug_1", "porcelain_mug_1"),
            ),
           )

    cfg4 = ("and",
            ("relaxedon", "red_coffee_mug_1", "plate_1"),
            ("and",
             ("relaxedon", "white_yellow_mug_1", "red_coffee_mug_1"),
             ("relaxedon", "porcelain_mug_1", "white_yellow_mug_1"),
            ),
           )

    cfg5 = ("and",
            ("relaxedon", "white_yellow_mug_1", "plate_1"),
            ("and",
             ("relaxedon", "porcelain_mug_1", "white_yellow_mug_1"),
             ("relaxedon", "red_coffee_mug_1", "porcelain_mug_1"),
            ),
           )

    cfg6 = ("and",
            ("relaxedon", "white_yellow_mug_1", "plate_1"),
            ("and",
             ("relaxedon", "red_coffee_mug_1", "white_yellow_mug_1"),
             ("relaxedon", "porcelain_mug_1", "red_coffee_mug_1"),
            ),
           )

    # Connect 6 possibilities with "or"
    tower_any_order = ("or",
                       cfg1,
                       ("or",
                        cfg2,
                        ("or",
                         cfg3,
                         ("or",
                          cfg4,
                          ("or", cfg5, cfg6)
                         )
                        )
                       )
                      )


    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[ "red_coffee_mug_1","porcelain_mug_1","white_yellow_mug_1","plate_1",],
        goal_states=[
            tower_any_order,
            ("upright", "red_coffee_mug_1"),
            ("upright", "porcelain_mug_1"),
            ("upright", "white_yellow_mug_1"),

            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()