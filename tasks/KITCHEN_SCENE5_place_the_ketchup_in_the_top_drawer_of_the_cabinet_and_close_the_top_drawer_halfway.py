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
    scene_name = "kitchen_scene5"
    language = "Place the ketchup in the top drawer of the cabinet and close the top drawer halfway"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "white_cabinet_1"],
        goal_states=[
            ("In", "ketchup_1", "white_cabinet_1_top_region"),
            ("OpenRatio", "white_cabinet_1_top_region", 0.5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
