# Run in the root of the repository
python motion_planning/collect_scripted_demonstration.py --bddl "libero/libero/bddl_files/libero_90/KITCHEN_SCENE1_put_the_black_bowl_on_the_plate.bddl" --robots Panda

python motion_planning/collect_demonstration.py --bddl "libero/libero/bddl_files/libero_90/KITCHEN_SCENE1_put_the_black_bowl_on_the_plate.bddl" --controller OSC_POSE --robots Panda --device keyboard