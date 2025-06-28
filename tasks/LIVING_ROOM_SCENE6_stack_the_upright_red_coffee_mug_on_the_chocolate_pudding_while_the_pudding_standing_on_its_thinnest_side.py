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
    scene_name = "living_room_scene6"
    language = "Stack the upright red coffee mug on the chocolate pudding while the pudding standing on its thinnest side"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["red_coffee_mug_1", "chocolate_pudding_1"],
        goal_states=[
            ("On", "red_coffee_mug_1", "chocolate_pudding_1"),
            ("Upright", "red_coffee_mug_1"),
            ("Or",
                ("AxisAlignedWithin", "chocolate_pudding_1", "x", 0, 10),
                ("AxisAlignedWithin", "chocolate_pudding_1", "x", 170, 180),
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
