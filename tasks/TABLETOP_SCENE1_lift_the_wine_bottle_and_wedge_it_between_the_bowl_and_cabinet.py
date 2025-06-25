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
    """Defines and registers the task with the libero environment."""
    scene_name = "tabletop_scene1"
    language = "Lift the wine bottle and wedge it between the bowl and cabinet"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
    "wine_bottle_1",
    "akita_black_bowl_1",
    "wooden_cabinet_1"
],
        goal_states=[
        ("ConstraintOnce", ("InAir", "wine_bottle_1", 0.90)),
        ("Any",(
            ("MidBetween", "akita_black_bowl_1", "wine_bottle_1", "wooden_cabinet_1", "x"),
            ("MidBetween", "akita_black_bowl_1", "wine_bottle_1", "wooden_cabinet_1", "y")
        )),
    ]
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(f"Generated BDDL files: {bddl_file_names}")
    if failures:
        print(f"Failures: {failures}")


if __name__ == "__main__":
    main()
