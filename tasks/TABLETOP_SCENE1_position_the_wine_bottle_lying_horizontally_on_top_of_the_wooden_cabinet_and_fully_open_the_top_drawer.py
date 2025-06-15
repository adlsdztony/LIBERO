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

from libero.libero.benchmark.mu_creation import TabletopScene1

def main():
    scene_name = "tabletop_scene1"
    language = "Position the wine bottle lying horizontally on top of the wooden cabinet and fully open the top drawer"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wine_bottle_1", 'wooden_cabinet_1'],
        goal_states=[
            ('RelaxedOn', 'wine_bottle_1', 'wooden_cabinet_1'),  
            ('Open', 'wooden_cabinet_1_top_region'),
            ("AxisAlignedWithin", "wine_bottle_1", "z", 85, 95)
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
