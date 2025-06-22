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

    scene_name = "kitchen_scene3"
    language = "Align the handles of the moka pot and the frypan, and ensure both stand upright on the table"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["moka_pot_1", "chefmate_8_frypan_1"],
        goal_states=[
            ("YawAngleAligned", "chefmate_8_frypan_1", "moka_pot_1", 10, 90),
            ("PositionWithin", "moka_pot_1",  0, 0, 0.96610586, 1.0, 1.0, 0.01),
            ("PositionWithin", "chefmate_8_frypan_1", 0, 0,  0.89917096, 1.0, 1.0, 0.01)
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
