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
    language = "Create a configuration where the top drawer contains one butter pack while the other butter pack supports the upside-down pudding"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=['butter_1', 'chocolate_pudding_1', 'butter_2', 'wooden_cabinet_1'],
        goal_states=[
            ('Or',
                ('And',
                    ('In', 'butter_1', 'wooden_cabinet_1_top_region'),
                    ('On', 'chocolate_pudding_1', 'butter_2'),
                ),
                ('And',
                    ('In', 'butter_2', 'wooden_cabinet_1_top_region'),
                    ('On', 'chocolate_pudding_1', 'butter_1'),
                ),
            ),
            ('UpsideDown', 'chocolate_pudding_1'),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()

