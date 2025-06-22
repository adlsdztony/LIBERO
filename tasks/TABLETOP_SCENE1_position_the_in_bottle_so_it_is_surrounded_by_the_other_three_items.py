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
    language = "Position the wine bottle so it is surrounded and contacted by the other three items. Please make sure that the orientation of the objects are unchanged and that the objects are on the table."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["wine_bottle_1", "cream_cheese_1", "plate_1", "akita_black_bowl_1"],
        goal_states=[
            ("InContact", "wine_bottle_1", "cream_cheese_1"),
            ("InContact", "wine_bottle_1", "plate_1"),
            ("InContact", "wine_bottle_1", "akita_black_bowl_1"),
            ("Not", ("InContact", "cream_cheese_1", "plate_1")),
            ("Not", ("InContact", "cream_cheese_1", "akita_black_bowl_1")),
            ("Not", ("InContact", "plate_1", "akita_black_bowl_1")),
            ("Upright", "wine_bottle_1"),
            ("Upright", "akita_black_bowl_1"),
            ("Upright", "plate_1"),
            ("Not", ("InAir", "wine_bottle_1", 0.898861)), # potential reward hacking: Wine bottle has to be on the table
            ("Not", ("InAir", "plate_1", 0.9024997)),
            ("Not", ("InAir", "cream_cheese_1", 0.908907)),
            ("Not", ("InAir", "akita_black_bowl_1", 0.898403)),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
