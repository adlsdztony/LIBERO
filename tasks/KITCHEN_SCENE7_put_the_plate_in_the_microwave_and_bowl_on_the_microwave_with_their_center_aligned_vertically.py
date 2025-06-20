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
    scene_name = "kitchen_scene7"
    language = "Put the plate in the microwave and bowl on the microwave with their center aligned vertically"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["white_bowl_1", "plate_1", "microwave_1"],
        goal_states=[
            ("In", "plate_1", "microwave_1_heating_region"),
            ("RelaxedOn", "white_bowl_1", "microwave_1"),
            ("PositionWithinObject", "white_bowl_1", "plate_1", -0.05, -0.05, -2, 0.05, 0.05, 2),
        ],
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
