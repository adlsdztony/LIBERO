"""This is a standalone file for create a task in libero."""
import numpy as np

from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
    get_task_info
)

from libero.libero.benchmark.mu_creation import *


def main():
    # living_room_scene_4
    scene_name = "living_room_scene4"
    language = "Position the salad dressing bottle in the wooden tray leaning against one of the bowls"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["new_salad_dressing_1", "wooden_tray_1","akita_black_bowl_1","akita_black_bowl_2"],
        goal_states=[
            ('In', 'new_salad_dressing_1', 'wooden_tray_1_contain_region'), 
            ('Or', ('InContact', 'new_salad_dressing_1', 'akita_black_bowl_1'),
             ('InContact', 'new_salad_dressing_1', 'akita_black_bowl_2')),
             ('Not', ('AxisAlignedWithin', 'new_salad_dressing_1', 'y', '0', '5')),
        ],
    )


    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
