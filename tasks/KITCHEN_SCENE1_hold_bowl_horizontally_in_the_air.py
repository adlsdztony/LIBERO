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

    scene_name = "kitchen_scene1"
    language = "Hold the bowl upright in the air and its opening faces horizontally."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "akita_black_bowl_1", "wooden_cabinet_1"],
        goal_states=[
            ("InAir", "akita_black_bowl_1", 0.2),
            ("Not", (
                "InContact", "akita_black_bowl_1", "plate_1"
            )),
            ("Not", (
                "InContact", "akita_black_bowl_1", "wooden_cabinet_1"
            )),
            ("AxisAlignedWithin", "akita_black_bowl_1", "z", 85, 95), # in degree
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()