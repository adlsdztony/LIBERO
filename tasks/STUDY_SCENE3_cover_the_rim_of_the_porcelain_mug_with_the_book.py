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

from libero.libero.benchmark.mu_creation import StudyScene3

def main():
    scene_name = "study_scene3"
    language = "Cover the rim of the porcelain mug with the book"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["black_book_1","porcelain_mug_1"],
        goal_states=[
            
            ("upright","porcelain_mug_1"),

            ("axisalignedwithin",
                "black_book_1", "z",
                80.0, 100.0),

            ("incontact",
                "black_book_1", "porcelain_mug_1"),

            ("posigreaterthanobject",
                "black_book_1", "porcelain_mug_1",
                "z", 0.01),
                
            ("relaxedon", "black_book_1", "porcelain_mug_1"),
                
                
                
                ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()