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


@register_mu(scene_type="kitchen")
class KitchenScene2(InitialSceneTemplates):
    def __init__(self):

        fixture_num_info = {
            "kitchen_table": 1,
            "wooden_cabinet": 1,
        }

        object_num_info = {
            "akita_black_bowl": 3,
        }

        super().__init__(
            workspace_name="kitchen_table",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.0, -0.30],
                region_name="wooden_cabinet_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
                yaw_rotation=(np.pi, np.pi),
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.05, 0.20],
                region_name="akita_black_bowl_middle_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.10, 0.15],
                region_name="akita_black_bowl_front_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.15, 0.05],
                region_name="akita_black_bowl_back_init_region",
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
            (
                "On",
                "akita_black_bowl_1",
                "kitchen_table_akita_black_bowl_front_init_region",
            ),
            (
                "On",
                "akita_black_bowl_2",
                "kitchen_table_akita_black_bowl_middle_init_region",
            ),
            (
                "On",
                "akita_black_bowl_3",
                "kitchen_table_akita_black_bowl_back_init_region",
            ),
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
        ]
        return states


def main():

    # Modified scene, remove the plate
    scene_name = "kitchen_scene2"
    language = "Arrange the three bowls so that their centers form an equilateral triangle"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
        goal_states=[
            ("Equal", ("Distance", "akita_black_bowl_1", "akita_black_bowl_2"), 
                      ("Distance", "akita_black_bowl_2", "akita_black_bowl_3"),
                      0.016),
            ("Equal", ("Distance", "akita_black_bowl_2", "akita_black_bowl_3"), 
                      ("Distance", "akita_black_bowl_1", "akita_black_bowl_3"),
                      0.016),
            ("Equal", ("GetPosi", "akita_black_bowl_1", "z"), 0.898, 0.001),
            ("Equal", ("GetPosi", "akita_black_bowl_2", "z"), 0.898, 0.001),
            ("Equal", ("GetPosi", "akita_black_bowl_3", "z"), 0.898, 0.001),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
