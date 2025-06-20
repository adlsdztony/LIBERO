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
    scene_name = "living_room_scene2"
    language = "Arrange the butter standing on its thinnest side and the alphabet soup upside down while keeping them in contact but both on the table"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1", "alphabet_soup_1"],
        goal_states=[
            ("InContact", "butter_1", "alphabet_soup_1"),
            ("Or",
                ("AxisAlignedWithin", "butter_1", "x", 0, 10),
                ("AxisAlignedWithin", "butter_1", "x", 160,180),
            ),
            ("AxisAlignedWithin", "alphabet_soup_1", "y", 160,180),
            ("PositionWithin", "butter_1", 0, 0, 0.48, 1.0, 1.0, 0.04),
            ("PositionWithin", "alphabet_soup_1", 0, 0, 0.48, 1.0, 1.0, 0.04),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()