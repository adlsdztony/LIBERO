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
    language = "Place the plate between the bowl and cheese so that it touches both items on the table."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["cream_cheese_1", 'akita_black_bowl_1', 'plate_1'],
        goal_states=[
            ('Any', (
                ('Between', 'akita_black_bowl_1', 'plate_1', 'cream_cheese_1', 'y'),
                ('Between', 'akita_black_bowl_1', 'plate_1', 'cream_cheese_1', 'x'),
                ('Between', 'cream_cheese_1', 'plate_1', 'akita_black_bowl_1', 'y'),
                ('Between', 'cream_cheese_1', 'plate_1', 'akita_black_bowl_1', 'x'),
            )),
            ('PosiLessThan', 'cream_cheese_1', 'z', 0.91),
            ('PosiLessThan', 'akita_black_bowl_1', 'z', 0.90),
            ('PosiLessThan', 'plate_1', 'z', 0.91),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
