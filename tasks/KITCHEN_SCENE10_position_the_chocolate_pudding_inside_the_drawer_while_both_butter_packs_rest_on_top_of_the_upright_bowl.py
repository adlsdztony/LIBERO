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

from libero.libero.benchmark.mu_creation import *

def main():

    scene_name = "kitchen_scene10"
    language = "Position the chocolate pudding inside the top drawer while both butter packs rest on top of the upright bowl"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=['butter_1', 'chocolate_pudding_1', 'butter_2', 'wooden_cabinet_1', "akita_black_bowl_1"],
        goal_states=[
            ('In', 'chocolate_pudding_1', 'wooden_cabinet_1_top_region'), 
            ('Upright', 'akita_black_bowl_1'), 
            ('RelaxedOn', 'butter_1', 'akita_black_bowl_1'), 
            ('RelaxedOn', 'butter_2', 'akita_black_bowl_1')
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()

