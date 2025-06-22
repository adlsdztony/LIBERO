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
    scene_name = "living_room_scene3"
    language = "Put all items in the tray without any item touching with each other"
    objects_of_interest=["alphabet_soup_1", "cream_cheese_1", "tomato_sauce_1", "ketchup_1", "butter_1", "wooden_tray_1"]
    items=objects_of_interest[:-1]
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=objects_of_interest,
        goal_states= [("RelaxedOn", item, "wooden_tray_1") for item in items]
                    +[("Not", ("InContact", item1, item2)) for item1 in  items for item2 in items if item1 != item2],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
