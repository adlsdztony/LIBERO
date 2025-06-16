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

    scene_name = "kitchen_scene10"
    language = "Create a linear arrangemen on the table with one butter pack between the bowl and the other butter pack"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "butter_1", "butter_2"],
        goal_states=[
            ('Linear', 'akita_black_bowl_1', 'butter_1', 'butter_2', 0.001),
            ("Any",
                (("relaxedbetween", 'akita_black_bowl_1', 'butter_1', 'butter_2', "x"),
                ("relaxedbetween", 'akita_black_bowl_1', 'butter_2', 'butter_1', "x"),
                ("relaxedbetween", 'akita_black_bowl_1', 'butter_1', 'butter_2', "y"),
                ("relaxedbetween", 'akita_black_bowl_1', 'butter_2', 'butter_1', "y"),)
            ),
            ("Equal", ("GetPosi", 'butter_1', "z"), 0.908, 0.001),
            ("Equal", ("GetPosi", 'butter_2', "z"), 0.908, 0.001),
            ("Equal", ("GetPosi", 'akita_black_bowl_1', "z"), 0.898, 0.001),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()