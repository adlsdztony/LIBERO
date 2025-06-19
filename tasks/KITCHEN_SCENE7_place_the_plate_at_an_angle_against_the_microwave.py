"""This is an exmaple file for creating a task in libero."""
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
    # kitchen_scene_1
    scene_name = "kitchen_scene7"
    language = "Place the plate at an angle against the microwave"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "microwave_1"],
        goal_states=[
            ("Or",
                ("AxisAlignedWithin", "plate_1", "z", 10, 80),
                ("AxisAlignedWithin", "plate_1", "z", 100, 170),
            ),
            ("InContact", "plate_1", "microwave_1"),
        ],
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
