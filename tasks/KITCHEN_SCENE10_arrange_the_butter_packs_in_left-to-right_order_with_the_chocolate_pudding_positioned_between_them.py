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
    language = "Arrange the butter packs in left-to-right order with the chocolate pudding positioned between them"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=['butter_1', 'chocolate_pudding_1', 'butter_2'],
        goal_states=[
            ('Linear', 'butter_1', 'chocolate_pudding_1', 'butter_2', 0.005),
            ('Or',
                ('Ordering', 'butter_1', 'chocolate_pudding_1', 'butter_2'),
                ('Ordering', 'butter_2', 'chocolate_pudding_1', 'butter_1')
            ),
            
            ('Not',
                ('InAir', 'butter_1', 0.92)
            ),
            ('Not',
                ('InAir', 'chocolate_pudding_1', 0.92)
            ),
            ('Not',
                ('InAir', 'butter_2', 0.92)
            ),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()

