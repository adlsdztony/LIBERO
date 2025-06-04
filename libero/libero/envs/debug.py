import numpy as np
import robosuite.utils.transform_utils as transform_utils

DEBUG = False

print_time = 0

def print_states(goal_state, results, object_states_dict):
    if not DEBUG:
        return
    
    global print_time

    if print_time % 100 != 0:
        print_time += 1
        return
    print("\033[?25l", end='')
    num_lines = len(goal_state) + 4 + len(object_states_dict) + 4 + 1

    # move cursor up num_lines lines if any previous output exists
    for _ in range(num_lines):
        print("\033[A", end='')
    
    predicate_str_len = 60
    print("┌" + "─" * predicate_str_len + "┬" + "─" * 10 + "┐")
    print("│" + "predicate".ljust(predicate_str_len) + "│" + "result".ljust(10) + "│")
    print("├" + "─" * predicate_str_len + "┼" + "─" * 10 + "┤")
    
    for i, (state, result) in enumerate(zip(goal_state, results)):
        state_str = str(state)
        if len(state_str) > predicate_str_len:
            state_str = state_str[:predicate_str_len-3] + "..."
        result_str = str(result)
        print("│" + state_str.ljust(predicate_str_len) +"│ " + result_str.ljust(8) + " │")
        
    print("└" + "─" * predicate_str_len + "┴" + "─" * 10 + "┘")

    # print the object states
    object_name_str_len = 30
    object_posi_str_len = 50
    object_rotation_str_len = 50
    print("Object states:"+" "* (object_name_str_len + object_posi_str_len + object_rotation_str_len - 15))
    print("┌" + "─" * object_name_str_len + "┬" + "─" * object_posi_str_len + "─" * object_rotation_str_len + "┐")
    print("│" + "object".ljust(object_name_str_len) + "│" + "posi".ljust(object_posi_str_len) + "│" + "rotation".ljust(object_rotation_str_len-1) + "│")
    print("├" + "─" * object_name_str_len + "┼" + "─" * object_posi_str_len + "─" * object_rotation_str_len + "┤")
    for object_name, object in object_states_dict.items():
        object_name_str = str(object_name)
        if len(object_name_str) > object_name_str_len:
            object_name_str = object_name_str[:object_name_str_len-3] + "..."
        geom = object.get_geom_state()
        object_state_str = str(geom["pos"])
        if len(object_state_str) > object_posi_str_len:
            object_state_str = object_state_str[:object_posi_str_len-3] + "..."
        w, x, y, z = geom["quat"]
        q_curr = np.array([x, y, z, w])
        R_curr = transform_utils.quat2mat(q_curr)
        object_rotation_str = str(R_curr[0, :])
        if len(object_rotation_str) > object_rotation_str_len:
            object_rotation_str = object_rotation_str[:object_rotation_str_len-3] + "..."
        print("│" + object_name_str.ljust(object_name_str_len) + "│" + object_state_str.ljust(object_posi_str_len) + "│" + object_rotation_str.ljust(object_rotation_str_len-1) + "│")
    print("└" + "─" * object_name_str_len + "┴" + "─" * object_posi_str_len + "─"* object_rotation_str_len + "┘")
    print_time += 1