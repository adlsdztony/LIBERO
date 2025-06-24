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

from libero.libero.benchmark.mu_creation import KitchenScene4

def main():
    scene_name = "kitchen_scene4"
    language = "Hold the wine bottle upright in the air and make its center aligned with bowl's center"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "wine_bottle_1"],
        goal_states=[
            ("above","wine_bottle_1", "akita_black_bowl_1"),
            ("upright","wine_bottle_1"),
            ("inair","wine_bottle_1", 0.15),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()