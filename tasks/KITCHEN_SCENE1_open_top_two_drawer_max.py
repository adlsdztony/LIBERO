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
    # kitchen_scene_1
    scene_name = "kitchen_scene1"
    language = "Open the top two drawers to their maximum extent"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wooden_cabinet_1"],
        goal_states=[
            ("OpenRatio", "wooden_cabinet_1_top_region", 1),
            ("OpenRatio", "wooden_cabinet_1_middle_region", 1),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()