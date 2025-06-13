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
    language = "Place the cream cheese between the milk and the butter in a horizontal arrangement, ensuring it touches both but is not stacked on top of either"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["milk_1", "butter_1", "cream_cheese_1"],
        goal_states=[
            ("Or",
                ("Between", "milk_1", "cream_cheese_1", "butter_1","y"),
                ("Between", "milk_1", "cream_cheese_1", "butter_1","x"),
            ),
            ("Equal", ("GetPosi", "cream_cheese_1", "z"), 0.445, 0.001),
            ("Equal", ("GetPosi", "milk_1", "z"), 0.506, 0.001),
            ("Equal", ("GetPosi", "butter_1", "z"), 0.445, 0.001),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
