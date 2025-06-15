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
    scene_name = "living_room_scene4"
    language = "Create a linear arrangement in the tray with the chocolate pudding positioned between the two bowls"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=['chocolate_pudding_1', 'wooden_tray_1', 'akita_black_bowl_1', 'akita_black_bowl_2'],
        goal_states=[
            ('In', 'akita_black_bowl_1', 'wooden_tray_1_contain_region'), 
            ('In', 'akita_black_bowl_2', 'wooden_tray_1_contain_region'), 
            ('In', 'chocolate_pudding_1', 'wooden_tray_1_contain_region'), 
            ('Linear', 'akita_black_bowl_1', 'akita_black_bowl_2', 'chocolate_pudding_1', 0.01),
            ('Or',
                ('Ordering', 'akita_black_bowl_1', 'chocolate_pudding_1', 'akita_black_bowl_2'),
                ('Ordering', 'akita_black_bowl_2', 'chocolate_pudding_1', 'akita_black_bowl_1')
            ),
            ]
    )


    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
