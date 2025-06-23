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
    scene_name = "kitchen_scene6"
    language = "Make the two mugs touch each other on the table"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "white_yellow_mug_1"],
        goal_states=[
            ("Not", ("InAir", "porcelain_mug_1", 0.9)),
            ("Not", ("InAir", "white_yellow_mug_1", 0.91)),
            ("InContact", "porcelain_mug_1", "white_yellow_mug_1"),       
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
