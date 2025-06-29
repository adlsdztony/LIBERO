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
    language = "Place both the ketchup and the bowl in the top drawer, touching each other, with the ketchup lying down."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "white_cabinet_1", "akita_black_bowl_1"],
        goal_states=[
            ("In", "ketchup_1", "white_cabinet_1_top_region"),
            ("In", "akita_black_bowl_1", "white_cabinet_1_top_region"),
            ("InContact", "ketchup_1", "akita_black_bowl_1"),
            ("Or",
                ("AxisAlignedWithin", "ketchup_1", "z", 170, 180),
                ("AxisAlignedWithin", "ketchup_1", "z", 0, 10)
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
