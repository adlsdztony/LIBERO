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
    language = "Rotate both butter 180 degrees horizontally and make them touch each other"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_2", "butter_1"],
        goal_states=[
            ("OrientedAtDegree", "butter_2", 0, 0, 0, 15, 15, 15),
            ("OrientedAtDegree", "butter_1", 0, 0, 0, 15, 15, 15),
            ("InContact", "butter_2", "butter_1"),
            ("Not", ("InAir", "butter_1", 0.91)),
            ("Not", ("InAir", "butter_2", 0.91)),


                    
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
