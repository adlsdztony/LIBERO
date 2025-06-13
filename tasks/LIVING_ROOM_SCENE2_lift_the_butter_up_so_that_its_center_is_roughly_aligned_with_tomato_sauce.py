"""This is a standalone file for create a task in libero."""
from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    generate_bddl_from_task_info,
)
import numpy as np

from libero.libero.benchmark.mu_creation import LivingRoomScene2

def main():
    scene_name = "living_room_scene2"
    language = "Lift the butter up so that its center is roughly aligned with tomato sauce"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1", "tomato_sauce_1"],
        goal_states=[
            ("Equal", ("GetPosi", "butter_1", "z"), ("GetPosi", "tomato_sauce_1", "z"), 0.02),
            ("Or",
                ("Equal", ("GetPosi", "butter_1", "x"), ("GetPosi", "tomato_sauce_1", "x"), 0.02),
                ("Equal", ("GetPosi", "butter_1", "y"), ("GetPosi", "tomato_sauce_1", "y"), 0.02)
            ),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()