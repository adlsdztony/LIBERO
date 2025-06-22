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

from libero.libero.benchmark.mu_creation import LivingRoomScene3

def main():

    scene_name = "living_room_scene3"
    language = "Place the butter on top of the cream cheese so that the two longer side edges are aligned, but one short front edge of the butter extends halfway beyond the cream cheese, creating a step-like overhang"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1", "cream_cheese_1"],
        goal_states=[
            ("RelaxedOn", "butter_1", "cream_cheese_1"),
            ("AxisAlignedWithin", "butter_1", "z", 0, 5),
            ("AxisAlignedWithin", "cream_cheese_1", "z", 0, 5),
            (
                "Any",
                (
                    ("PositionWithinObject", "butter_1", "cream_cheese_1", 0.02, -0.01, 0, 0.05, 0.01, 0.02),
                    ("PositionWithinObject", "butter_1", "cream_cheese_1", -0.05, -0.01, 0, -0.02, 0.01, 0.02),
                )
            )
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
