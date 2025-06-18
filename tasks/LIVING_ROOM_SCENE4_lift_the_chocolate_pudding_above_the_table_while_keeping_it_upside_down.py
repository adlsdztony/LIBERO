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
    language = "Lift the chocolate pudding above the table while keeping it upside down"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=['chocolate_pudding_1', 'new_salad_dressing_1', 'akita_black_bowl_1', 'akita_black_bowl_2'],
        goal_states=[
            ('InAir', 'chocolate_pudding_1', 0.4511),
            ('UpsideDown', 'chocolate_pudding_1'),
            ('Not', ('RelaxedOn', 'chocolate_pudding_1', 'akita_black_bowl_1')),
            ('Not', ('RelaxedOn', 'chocolate_pudding_1', 'akita_black_bowl_2')),
            ('Not', ('RelaxedOn', 'chocolate_pudding_1', 'new_salad_dressing_1')),       
            ]
    )


    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
