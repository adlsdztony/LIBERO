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
    language = "Hold the chocolate pudding directly above the bowl with their center aligned"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chocolate_pudding_1", "akita_black_bowl_1"],
        goal_states=[
            ("InAir", "chocolate_pudding_1", 0.915),
            ("And",
                ("PosiSameWith", "chocolate_pudding_1", "akita_black_bowl_1", "x", 0.02),
                ("PosiSameWith", "chocolate_pudding_1", "akita_black_bowl_1", "y", 0.02)
            ),         
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
