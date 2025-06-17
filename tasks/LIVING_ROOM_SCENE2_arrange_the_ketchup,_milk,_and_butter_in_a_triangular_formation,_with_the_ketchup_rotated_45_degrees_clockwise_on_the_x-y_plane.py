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
    language = "Arrange the ketchup, milk, and butter in a triangular formation, with the ketchup rotated 45 degrees clockwise on the x-y plane"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "milk_1", "butter_1"],
        goal_states=[
            ("AxisAlignedWithinWorldAxis", "ketchup_1", "z", 40, 50, 'y'),
            ("Not", ("Linear", "ketchup_1", "milk_1", "butter_1", 0.01)),
            ("Equal", ("GetPosi", "ketchup_1", "z"), 0.509, 0.001),
            ("Equal", ("GetPosi", "milk_1", "z"), 0.506, 0.001),
            ("Equal", ("GetPosi", "butter_1", "z"), 0.445, 0.001),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
