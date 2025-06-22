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
    language = "Flip the plate upside down and place the chocolate pudding on top of it"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "chocolate_pudding_1"],
        goal_states=[
            ("UpsideDown", "plate_1"),
            ("On", "chocolate_pudding_1", "plate_1"),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
