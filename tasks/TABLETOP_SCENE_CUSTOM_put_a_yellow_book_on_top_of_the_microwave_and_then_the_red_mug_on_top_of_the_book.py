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

@register_mu(scene_type="tabletop_manipulation")
class TabletopSceneCustom(InitialSceneTemplates):
    """
    A large, multi-purpose table in a small studio apartment, serving as
    both a work desk and a kitchenette. This environment is designed to
    generate a high volume of diverse tasks by creating a natural conflict
    between a "Desk Zone" and a "Kitchenette Zone" on the same surface.
    """
    def __init__(self):

        # Total of 4 fixtures (including the table itself) and 11 movable objects
        fixture_num_info = {
            "table": 1,
            "microwave": 1,
            "wooden_shelf": 1,
            "wooden_cabinet": 1,
        }

        object_num_info = {
            "black_book": 2,
            "yellow_book": 1,
            "white_storage_box": 1,
            "red_coffee_mug": 1,
            "porcelain_mug": 1,
            "plate": 1,
            "cookies": 1,
            "milk": 1,
            "macaroni_and_cheese": 1,
        }

        super().__init__(
            workspace_name="main_table",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):
        # The table is conceptually split into two zones:
        # Left side (x < 0) is the "Desk Zone"
        # Right side (x > 0) is the "Kitchenette Zone"

        # --- DESK ZONE REGIONS (Left Side) ---
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.10, 0.35],
                region_name="desk_zone_shelf_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.17, -0.45],
                region_name="desk_zone_cabinet_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
                yaw_rotation=(np.pi, np.pi),
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.40, -0.10-0.10+0.05],
                region_name="desk_zone_book_1_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.40, -0.10+0.10+0.05],
                region_name="desk_zone_book_2_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.40, -0.10+0.05],
                region_name="desk_zone_book_3_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.40, -0.40],
                region_name="desk_zone_storage_box_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )

        # --- KITCHENETTE ZONE REGIONS (Right Side) ---
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.25, 0.4],
                region_name="kitchen_zone_microwave_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.20-0.10, 0.25],
                region_name="kitchen_zone_plate_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.05, 0.05-0.10],
                region_name="kitchen_zone_milk_region",
                target_name=self.workspace_name,
                region_half_len=0.05,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.05-0.10, 0.15-0.10],
                region_name="kitchen_zone_cookies_region",
                target_name=self.workspace_name,
                region_half_len=0.05,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0, 0.15-0.10],
                region_name="kitchen_zone_macaroni_region",
                target_name=self.workspace_name,
                region_half_len=0.05,
            )
        )

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    @property
    def init_states(self):
        states = [
            # Place Desk Zone fixtures and objects
            ("On", "wooden_shelf_1", "main_table_desk_zone_shelf_region"),
            ("On", "wooden_cabinet_1", "main_table_desk_zone_cabinet_region"),
            ("On", "black_book_1", "main_table_desk_zone_book_1_region"),
            ("On", "black_book_2", "main_table_desk_zone_book_2_region"),
            ("On", "yellow_book_1", "main_table_desk_zone_book_3_region"),
            ("On", "white_storage_box_1", "main_table_desk_zone_storage_box_region"),
            ("On", "red_coffee_mug_1", "microwave_1_top_side"),
            # Place Kitchenette Zone fixtures and objects
            ("On", "microwave_1", "main_table_kitchen_zone_microwave_region"),
            ("On", "porcelain_mug_1", "wooden_cabinet_1_top_side"),
            ("On", "plate_1", "main_table_kitchen_zone_plate_region"),
            ("On", "cookies_1", "main_table_kitchen_zone_cookies_region"),
            ("On", "milk_1", "main_table_kitchen_zone_milk_region"),
            ("On", "macaroni_and_cheese_1", "main_table_kitchen_zone_macaroni_region"),
            
            # Set initial states for articulated objects
            ("Close", "microwave_1"),
        ]
        return states


def main():

    scene_name = "tabletop_scene_custom"
    language = "Put a yellow book on top of the microwave, and then the red mug on top of the book."
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=[
            "yellow_book_1", "red_coffee_mug_1"
        ],
        goal_states=[
            ("RelaxedOn", "yellow_book_1", "microwave_1"),
            ("RelaxedOn", "red_coffee_mug_1", "yellow_book_1"),                    
        ],   
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()

