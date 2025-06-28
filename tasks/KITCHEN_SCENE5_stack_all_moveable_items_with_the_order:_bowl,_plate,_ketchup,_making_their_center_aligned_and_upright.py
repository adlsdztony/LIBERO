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
    language = "Stack all moveable items with the order: bowl, plate, ketchup, making their center aligned and upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "plate_1", "white_cabinet_1", "ketchup_1"],
        goal_states=[
            ("On", "plate_1", "akita_black_bowl_1"),
            ("On", "ketchup_1", "plate_1"),
            ("Upright", "akita_black_bowl_1"),
            ("Upright", "plate_1"),
            ("AxisAlignedWithin", "ketchup_1", "z", 87, 93),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
