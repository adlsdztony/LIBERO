"""This is a standalone file for create a task in libero."""
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
    # kitchen_scene_2
    scene_name = "kitchen_scene2"
    language = "Place the plate upside down on the table with its bottom facing upward"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1"],
        goal_states=[
            ("Not", ("inair", "plate_1", 1)),
            ("UpsideDown", "plate_1")
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
