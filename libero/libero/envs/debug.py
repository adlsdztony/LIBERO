import numpy as np
import robosuite.utils.transform_utils as transform_utils
import os

DEBUG = os.getenv("LIBERO_DEBUG", "0") in ["1", "true", "True", "TRUE"]

def print_states(goal_state, results, object_states_dict, debug_time):
    if not DEBUG:
        return

    if debug_time % 100 != 0:
        return
    
    if debug_time == 0:
        print("\033c", end='')

    print("\033[?25l", end='')
    num_lines = len(goal_state) + 4 + len(object_states_dict) + 4 + 3

    for _ in range(num_lines):
        print("\033[A", end='')
    
    print("Detect time:", debug_time)
    predicate_str_len = 60
    print("┌" + "─" * predicate_str_len + "┬" + "─" * 50 + "┐")
    print("│" + " predicate".ljust(predicate_str_len) + "│" + " result".ljust(50) + "│")
    print("├" + "─" * predicate_str_len + "┼" + "─" * 50 + "┤")
    
    for i, (state, result) in enumerate(zip(goal_state, results)):
        state_str = str(state)
        if len(state_str) > predicate_str_len:
            state_str = state_str[:predicate_str_len-3] + "..."
        result_str = str(result)
        print("│" + state_str.ljust(predicate_str_len) +"│" + result_str.ljust(50) + "│")
        
    print("└" + "─" * predicate_str_len + "┴" + "─" * 50 + "┘")

    # print the object states
    object_name_str_len = 30
    object_posi_str_len = 50
    object_rotation_str_len = 45
    print("Object states:"+" "* (object_name_str_len + object_posi_str_len + object_rotation_str_len - 15))
    print("┌" + "─" * object_name_str_len + "┬" + "─" * object_posi_str_len + "─" * object_rotation_str_len + "-" * object_rotation_str_len + "-" * object_rotation_str_len + "┐")
    print("│" + " object".ljust(object_name_str_len) + "│" + " posi".ljust(object_posi_str_len) + "│" + " rotation_z".ljust(object_rotation_str_len-1) + "│" + "rotation_x".ljust(object_rotation_str_len-1) + "│" + "rotation_y".ljust(object_rotation_str_len-1) + "│")
    print("├" + "─" * object_name_str_len + "┼" + "─" * object_posi_str_len + "─" * object_rotation_str_len + "-" * object_rotation_str_len + "-" * object_rotation_str_len + "┤")
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
        object_rotation_z = R_curr[2] # value is like [-1.25680444e-05, -2.01587281e-05, 1.00000000e+00]
        # take only 3 digits after the decimal point while keeping the sign and the scientific notation
        object_rotation_z_str = str([f"{val:.3e}" for val in R_curr[2]])
        object_rotation_x_str = str([f"{val:.3e}" for val in R_curr[0]])
        object_rotation_y_str = str([f"{val:.3e}" for val in R_curr[1]])
        if len(object_rotation_z_str) > object_rotation_str_len:
            object_rotation__z_str = object_rotation_z_str[:object_rotation_str_len-3] + "..."
        if len(object_rotation_x_str) > object_rotation_str_len:
            object_rotation_x_str = object_rotation_x_str[:object_rotation_str_len-3] + "..."
        if len(object_rotation_y_str) > object_rotation_str_len:
            object_rotation_y_str = object_rotation_y_str[:object_rotation_str_len-3] + "..."
        print("│" + object_name_str.ljust(object_name_str_len) + "│" + object_state_str.ljust(object_posi_str_len) + "│" + object_rotation_z_str.ljust(object_rotation_str_len-1) + "│" + object_rotation_x_str.ljust(object_rotation_str_len-1) + "│" + object_rotation_y_str.ljust(object_rotation_str_len-1) + "│")
    print("└" + "─" * object_name_str_len + "┴" + "─" * object_posi_str_len + "─"* object_rotation_str_len + "─"* object_rotation_str_len + "─"* object_rotation_str_len + "┘")
