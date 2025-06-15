"""This is a standalone file for create a task in libero."""
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

    scene_name = "tabletop_scene1"
    language = "stack the cream cheese on top of the akita bowl with both items upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["cream_cheese_1", "akita_black_bowl_1", "wine_bottle_1", "plate_1"],
        goal_states=[
            ("RelaxedOn", "cream_cheese_1", "akita_black_bowl_1"),
            ("Upright", "cream_cheese_1"),
            ("Upright", "akita_black_bowl_1"),
            ("Not", ("RelaxedOn", "akita_black_bowl_1", "cream_cheese_1")),
            ("Not", ("RelaxedOn", "wine_bottle_1", "akita_black_bowl_1")),
            ("Not", ("RelaxedOn", "plate_1", "akita_black_bowl_1")),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main() 