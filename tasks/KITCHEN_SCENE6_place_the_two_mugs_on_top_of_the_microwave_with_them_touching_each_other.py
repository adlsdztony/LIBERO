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
    language = "Place the two mugs on top of the microwave with them touching each other"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["porcelain_mug_1", "white_yellow_mug_1","microwave_1"],
        goal_states=[
            ("RelaxedOn", "porcelain_mug_1", "microwave_1"),
            ("RelaxedOn", "white_yellow_mug_1", "microwave_1"),
            ("InContact", "porcelain_mug_1", "white_yellow_mug_1"),       
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
