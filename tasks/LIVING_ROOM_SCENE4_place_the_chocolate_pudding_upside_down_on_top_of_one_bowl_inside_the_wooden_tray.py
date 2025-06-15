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
    language = "Place the chocolate pudding upside down on top of one bowl inside the wooden tray"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=['chocolate_pudding_1', 'wooden_tray_1', 'akita_black_bowl_1', 'akita_black_bowl_2'],
        goal_states=[
            ('UpsideDown', 'chocolate_pudding_1'),
            ('Or',
                ('And',
                    ('In', 'akita_black_bowl_1', 'wooden_tray_1_contain_region'), 
                    ('RelaxedOn', 'chocolate_pudding_1', 'akita_black_bowl_1'), 
                ),
                ('And',
                    ('In', 'akita_black_bowl_2', 'wooden_tray_1_contain_region'), 
                    ('RelaxedOn', 'chocolate_pudding_1', 'akita_black_bowl_2'), 
                )
            ),
            ]
    )


    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
