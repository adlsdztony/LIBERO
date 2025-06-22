"""This is a standalone file for creating a task in libero."""
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

@register_mu(scene_type="kitchen")
class KitchenScene5(InitialSceneTemplates):
    def __init__(self):

        fixture_num_info = {
            "kitchen_table": 1,
            "white_cabinet": 1,
        }

        object_num_info = {
            "akita_black_bowl": 1,
            "plate": 1,
            "ketchup": 1,
        }

        super().__init__(
            workspace_name="kitchen_table",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.30],
                region_name="white_cabinet_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, 0.0],
                region_name="three_goal_region",
                target_name=self.workspace_name,
                region_half_len=100.0,  # Large region to ensure the book is in contact
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.03, -0.05],
                region_name="akita_black_bowl_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.10, -0.10],
                region_name="ketchup_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.05, -0.25],
                region_name="plate_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )
        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    @property
    def init_states(self):
        states = [
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),
            ("On", "plate_1", "kitchen_table_plate_init_region"),
            ("On", "white_cabinet_1", "kitchen_table_white_cabinet_init_region"),
            ("On", "ketchup_1", "kitchen_table_ketchup_init_region"),
            ("Open", "white_cabinet_1_top_region"),
        ]
        return states


def main():
    # Write your reward code here
    scene_name = "kitchen_scene5"
    language = "Make ketchup and bowl touch each other while keeping them upright"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["ketchup_1", "akita_black_bowl_1"],
        goal_states=[
            ("InContact", "ketchup_1", "akita_black_bowl_1"),
            ("On", "ketchup_1", "kitchen_table_three_goal_region"),
            ("On", "akita_black_bowl_1", "kitchen_table_three_goal_region"),
            ("AxisAlignedWithin", "ketchup_1", "y", 0, 5),
            ("AxisAlignedWithin", "akita_black_bowl_1", "z", 0, 5),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
