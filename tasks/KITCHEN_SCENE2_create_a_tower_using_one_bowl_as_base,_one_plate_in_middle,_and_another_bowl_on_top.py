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
    scene_name = "kitchen_scene2"
    language = "Create a tower using one bowl as base, one plate in middle, and another bowl on top"
    bowls = ["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"]
    plate = "plate_1"
    goal_states = [
        ("Any", tuple(
            ("And",
                ("RelaxedOn", plate, base_bowl),
                ("RelaxedOn", top_bowl, plate),
            )
            for base_bowl in bowls for top_bowl in bowls if base_bowl != top_bowl
        ))
    ]
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[plate] + bowls,
        goal_states=goal_states,
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()