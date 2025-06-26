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

from libero.libero.benchmark.mu_creation import TabletopScene1

def main():
    scene_name = "tabletop_scene1"
    language = "Place the cream cheese rotated 90 degrees clockwise horizontally on the top level of the wine rack"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["cream_cheese_1", 'wine_rack_1'],
        goal_states=[
            ("On", "cream_cheese_1", "wine_rack_1_top_region"),
            ("OrientedAtDegree", "cream_cheese_1", 0.0, 0.0, 90.0, 45.0, 360.0, 5.0)
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
