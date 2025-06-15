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

from libero.libero.benchmark.mu_creation import LivingRoomScene2

def main():
    scene_name = "living_room_scene2"
    language = "Position the butter and cream cheese block both upside down with their long axes parallel to each other"

    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["butter_1","cream_cheese_1"],
        goal_states=[
            ("UpsideDown", "butter_1"),
            ("UpsideDown", "cream_cheese_1"),
            
            # Due to the limited action of the robot, to complete the upsidedown action, 
            # you need to first select 90 ° clockwise or counterclockwise around the Z axis, 
            # and then rotate 180 ° around the X axis or Y axis.
            ("Or",
                (
                "Or",
                ("OrientedAtDegree", "butter_1", 180.0, 0.0, 90.0, 5.0, 5.0, 5.0),
                ("OrientedAtDegree", "butter_1", 180.0, 0.0, -90.0, 5.0, 5.0, 5.0)
                ),
                (
                "Or",
                ("OrientedAtDegree", "butter_1", 0.0, 180.0, 90.0, 5.0, 5.0, 5.0),
                ("OrientedAtDegree", "butter_1", 0.0, 180.0, -90.0, 5.0, 5.0, 5.0)
                )
    
            ),
            ("Or",
             ("Or",
                ("OrientedAtDegree", "cream_cheese_1", 180.0, 0.0, 90.0, 5.0, 5.0, 5.0),
                ("OrientedAtDegree", "cream_cheese_1", 180.0, 0.0, -90.0, 5.0, 5.0, 5.0)
                ),
                ("Or",
                ("OrientedAtDegree", "cream_cheese_1", 0.0, 180.0, 90.0, 5.0, 5.0, 5.0),
                ("OrientedAtDegree", "cream_cheese_1", 0.0, 180.0, -90.0, 5.0, 5.0, 5.0)
                )
                
            ),
            
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()