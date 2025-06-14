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
    language = "Line up the cream cheese between the butter and milk while keeping all items upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["cream_cheese_1", "butter_1", "milk_1"],
        goal_states=[
            ("AxisAlignedWithin", "cream_cheese_1", "z", 89, 91),
            ("AxisAlignedWithin", "butter_1", "z", 89, 91),
            ("AxisAlignedWithin", "milk_1", "y", 0, 3),
            ("Linear", "butter_1", "cream_cheese_1", "milk_1", 0.001),
            ("Or", ("RelaxedBetween", "butter_1", "cream_cheese_1", "milk_1", "x"), ("RelaxedBetween", "butter_1", "cream_cheese_1", "milk_1", "y")),
            ("PosiLessThan", "cream_cheese_1", "z", 0.48),
            ("PosiLessThan", "butter_1", "z", 0.48),
            ("PosiLessThan", "milk_1", "z", 0.507),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
