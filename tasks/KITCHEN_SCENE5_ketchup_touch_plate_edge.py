from libero.libero.benchmark.mu_creation import KitchenScene5
from libero.libero.utils.task_generation_utils import (
    generate_bddl_from_task_info,
    register_task_info,
)


def main():
    register_task_info(
        language="Move the ketchup bottle to touch the plate's edge while keeping it off the plate",
        scene_name="kitchen_scene5",
        objects_of_interest=["ketchup_1", "plate_1"],
        goal_states=[
            ("InContact", "ketchup_1", "plate_1"),  # Bottle must touch the plate
            ("Not", ("RelaxedOn", "ketchup_1", "plate_1")),  # Bottle must not be on top of the plate
        ],
    )
    bddl, _ = generate_bddl_from_task_info()
    print(bddl)


if __name__ == "__main__":
    main()