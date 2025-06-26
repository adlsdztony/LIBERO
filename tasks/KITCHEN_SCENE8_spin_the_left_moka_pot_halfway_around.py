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
    # Note: moka_pot_2 is the left moka pot
    scene_name = "kitchen_scene8"
    language = "Spin the left moka pot halfway around"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["moka_pot_1", "moka_pot_2", "flat_stove_1"],
        goal_states=[
            ("AxisAlignedWithinWorldAxis", "moka_pot_2", "x", 0, 10, "x"),
        ],
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
