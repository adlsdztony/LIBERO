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
class KitchenScene8(InitialSceneTemplates):
    def __init__(self):

        fixture_num_info = {
            "kitchen_table": 1,
            "flat_stove": 1,
        }

        object_num_info = {"moka_pot": 2}

        super().__init__(
            workspace_name="kitchen_table",
            fixture_num_info=fixture_num_info,
            object_num_info=object_num_info,
        )

    def define_regions(self):
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.20, -0.20],
                region_name="flat_stove_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.05, 0.25],
                region_name="moka_pot_right_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.05, 0.05],
                region_name="moka_pot_left_init_region",
                target_name=self.workspace_name,
                region_half_len=0.025,
            )
        )

        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0, 0],
                region_name="tabletop_region",
                target_name=self.workspace_name,
                region_half_len=0.46,
            )
        )

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    @property
    def init_states(self):
        states = [
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "moka_pot_1", "kitchen_table_moka_pot_right_init_region"),
            ("On", "moka_pot_2", "kitchen_table_moka_pot_left_init_region"),
            ("Turnon", "flat_stove_1"),
        ]
        return states


def main():
    scene_name = "kitchen_scene8"
    language = "Place the two moka pot right next to and touching each other"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["moka_pot_1", "moka_pot_2", "flat_stove_1"],
        goal_states=[
            ("On", "moka_pot_1", "kitchen_table_tabletop_region"),
            ("On", "moka_pot_2", "kitchen_table_tabletop_region"),
            ("InContact", "moka_pot_1", "moka_pot_2"),
        ],
    )
    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)

if __name__ == "__main__":
    main()
