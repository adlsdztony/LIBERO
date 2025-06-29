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
    language = "Lay both mugs down while keeping them in touch with each other on the table"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["white_yellow_mug_1", "porcelain_mug_1", "microwave_1"],
        goal_states=[
            ("Not", ("InAir", "white_yellow_mug_1", 0.97)),
            ("Not", ("InAir", "porcelain_mug_1", 0.97)),
            ("AxisAlignedWithin", "white_yellow_mug_1", "z", 80, 10),
            ("AxisAlignedWithin", "porcelain_mug_1", "z", 80, 100),
            ("InContact", "white_yellow_mug_1", "porcelain_mug_1"),

        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
