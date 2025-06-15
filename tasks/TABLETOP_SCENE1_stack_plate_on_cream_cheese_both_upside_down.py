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
    language = "Stack the plate on the cream cheese with both items positioned upside down"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["plate_1", "cream_cheese_1"],
        goal_states=[
            ("On", "plate_1", "cream_cheese_1"),
            ("UpsideDown", "plate_1"),
            ("UpsideDown", "cream_cheese_1")
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
