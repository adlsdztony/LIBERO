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

from libero.libero.benchmark.mu_creation import *

def main():

    scene_name = "kitchen_scene10"
    language = "Place both butter packs inside one of the drawers with one stacked on top of the other"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_cabinet_1", "butter_1", "butter_2"],
        goal_states=[
            ("Or",
                ('On', 'butter_1', 'butter_2'),
                ('On', 'butter_2', 'butter_1')
            ),
            ("Any",
                (("And",
                    ('In', 'butter_1', 'wooden_cabinet_1_top_region'),
                    ('In', 'butter_2', 'wooden_cabinet_1_top_region')
                ),
                ("And",
                    ('In', 'butter_1', 'wooden_cabinet_1_middle_region'),
                    ('In', 'butter_2', 'wooden_cabinet_1_middle_region')
                ),
                ("And",
                    ('In', 'butter_1', 'wooden_cabinet_1_bottom_region'),
                    ('In', 'butter_2', 'wooden_cabinet_1_bottom_region')
                ))
            ),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
