from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    generate_bddl_from_task_info,
    register_task_info,
)

from libero.libero.benchmark.mu_creation import StudyScene4

def main():
    scene_name = "study_scene4"
    language = "Pick up the porcelain mug, flip it upside down, and hold it directly above the red cup."
    register_task_info(
        language=language,
        scene_name=scene_name,
        objects_of_interest=["red_coffee_mug_1", "porcelain_mug_1"],
        goal_states=[
            ("upsidedown", "porcelain_mug_1"),
            ("above", "porcelain_mug_1", "red_coffee_mug_1"),
        ],
    )

    bddl, _ = generate_bddl_from_task_info()
    print(bddl)


if __name__ == "__main__":
    main()
