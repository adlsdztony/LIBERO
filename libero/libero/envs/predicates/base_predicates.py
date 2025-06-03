from typing import List
import numpy as np
import robosuite.utils.transform_utils as transform_utils
from libero.libero.envs.object_states.base_object_states import BaseObjectState


class Expression:
    def __init__(self):
        raise NotImplementedError

    def __call__(self):
        raise NotImplementedError


class UnaryAtomic(Expression):
    def __init__(self):
        pass

    def __call__(self, arg1):
        raise NotImplementedError
    
    def expected_arg_types(self) -> List[type]:
        raise NotImplementedError


class BinaryAtomic(Expression):
    def __init__(self):
        pass

    def __call__(self, arg1, arg2):
        raise NotImplementedError
    
    def expected_arg_types(self) -> List[type]:
        raise NotImplementedError


class MultiarayAtomic(Expression):
    def __init__(self):
        pass

    def __call__(self, *args):
        raise NotImplementedError
    
    def expected_arg_types(self) -> List[type]:
        raise NotImplementedError


class TruePredicateFn(MultiarayAtomic):
    def __init__(self):
        super().__init__()

    def __call__(self, *args):
        return True

    def expected_arg_types(self):
        return []


class FalsePredicateFn(MultiarayAtomic):
    def __init__(self):
        super().__init__()

    def __call__(self, *args):
        return False

    def expected_arg_types(self):
        return []


class Not(UnaryAtomic):
    def __call__(self, arg):
        return not arg

    def expected_arg_types(self):
        return [bool]


class And(BinaryAtomic):
    def __call__(self, arg1, arg2):
        return arg1 and arg2

    def expected_arg_types(self):
        return [bool, bool]


class Or(BinaryAtomic):
    def __call__(self, arg1, arg2):
        return arg1 or arg2

    def expected_arg_types(self):
        return [bool, bool]


class Any(UnaryAtomic):
    def __call__(self, arg):
        if not isinstance(arg, tuple):
            raise TypeError("Any expects a tuple of booleans")
        return any(arg)

    def expected_arg_types(self):
        return [tuple]


class All(UnaryAtomic):
    def __call__(self, arg):
        if not isinstance(arg, tuple):
            raise TypeError("All expects a list or tuple of booleans")
        return all(arg)

    def expected_arg_types(self):
        return [tuple]



class InContactPredicateFn(BinaryAtomic):
    def __call__(self, arg1, arg2):
        return arg1.check_contact(arg2)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class In(BinaryAtomic):
    def __call__(self, arg1, arg2):
        return arg2.check_contact(arg1) and arg2.check_contain(arg1)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class On(BinaryAtomic):
    """
    With 3cm center alignement constraint (original)
    """
    def __call__(self, arg1, arg2):
        return arg2.check_ontop(arg1)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]

class RelaxedOn(BinaryAtomic):
    """
    Without center alignment constraint
    """
    def __call__(self, arg1, arg2):
        return arg2.check_ontop(arg1, threshold=float('inf'))

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class PositionWithin(UnaryAtomic):
    def __call__(self, arg, pos_x, pos_y, pos_z, t_x, t_y, t_z):
        """
        Check if the object's position is within a certain threshold of a specified position.
        
        HINT: You may teleoperate and print out the current position and the target position to get a sense of the position
        
        Args:
            arg: The object to check.
            position: three floats pos_x, pos_y, pos_z coordinates to compare against.
            threshold: three floats t_x, t_y, t_z thresholds for proximity. Default is (0.01, 0.01, 0.01).
        
        Returns:
            bool: True if the object's position is within the threshold of the specified position, False otherwise.
        """
        geom = arg.get_geom_state()
        pos = geom["pos"]
        # Check if the position is within the specified threshold
        within_x = abs(pos[0] - pos_x) <= t_x
        within_y = abs(pos[1] - pos_y) <= t_y
        within_z = abs(pos[2] - pos_z) <= t_z
        
        # print current position, target position, and threshold
        # print(f"Current Position: {pos}, Target Position: {position}, Threshold: {threshold}")
        # print(f"Within X: {within_x}, Within Y: {within_y}, Within Z: {within_z}")
        return within_x and within_y and within_z
    
    def expected_arg_types(self):
        return [BaseObjectState, float, float, float, float, float, float]


class Under(BinaryAtomic):
    def __call__(self, arg1, arg2):
        return arg1.get_geom_state()["pos"][2] <= arg2.get_geom_state()["pos"][2]

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class Up(UnaryAtomic):
    def __call__(self, arg1):
        return arg1.get_geom_state()["pos"][2] >= 1.0

    def expected_arg_types(self):
        return [BaseObjectState]


class UpsideDown(UnaryAtomic):
    def __call__(self, arg):
        geom = arg.get_geom_state()
        w, x, y, z = geom["quat"]
        q_curr = np.array([x, y, z, w])
        R_curr = transform_utils.quat2mat(q_curr)
        z_curr = R_curr[:, 2]
        return z_curr[2] < -0.95

    def expected_arg_types(self):
        return [BaseObjectState]


class Upright(UnaryAtomic):
    def __call__(self, arg):
        geom = arg.get_geom_state()
        w, x, y, z = geom["quat"]
        quat_for_rs = np.array([x, y, z, w])
        R = transform_utils.quat2mat(quat_for_rs)
        z_axis_world = R[:, 2]
        return z_axis_world[2] >= 0.9

    def expected_arg_types(self):
        return [BaseObjectState]


class PosiGreaterThan(UnaryAtomic):
    """Check if the object's position is greater than a specified value along a specified axis."""
    def __call__(self, *args):
        arg, axis, value = args
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")

        pos = arg.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        return pos[axis_index] > value
    
    def expected_arg_types(self):
        return [BaseObjectState, str, float]

class AxisAlignedWithin(UnaryAtomic):
    """
    Check if the object's specified axis is within a degree range [min_deg, max_deg]
    from alignment with the world Z+ axis.

    Usage: Upright()(object, axis, min_deg, max_deg)
    """

    def __call__(self, *args):
        if len(args) != 4:
            raise ValueError("Upright expects 4 arguments: object, axis ('x', 'y', 'z'), min_degree, max_degree")
        obj, axis, min_deg, max_deg = args
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")
        if not (0 <= min_deg <= max_deg <= 180):
            raise ValueError("Degrees must satisfy 0 <= min_deg <= max_deg <= 180")

        min_rad = np.radians(min_deg)
        max_rad = np.radians(max_deg)
        cos_min = np.cos(min_rad)
        cos_max = np.cos(max_rad)

        geom = obj.get_geom_state()
        w, x, y, z = geom["quat"]
        quat_for_rs = np.array([x, y, z, w])
        R = transform_utils.quat2mat(quat_for_rs)

        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        object_axis_world = R[:, axis_index]
        cos_angle = object_axis_world[2]

        return cos_max <= cos_angle <= cos_min

    def expected_arg_types(self):
        return [BaseObjectState, str, float, float]


class Stack(BinaryAtomic):
    def __call__(self, arg1, arg2):
        return (
            arg1.check_contact(arg2)
            and arg2.check_contain(arg1)
            and arg1.get_geom_state()["pos"][2] > arg2.get_geom_state()["pos"][2]
        )

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class StackBowl(BinaryAtomic):
    """
    Check if two objects are stacked on top of each other, ensuring that they are 
    horizontally aligned and vertically separated within a defined range.

    Usage: StackBowl()(object1, object2)
    Arguments:
    - object1: The first object that needs to be checked for stacking.
    - object2: The second object that needs to be checked for stacking.
    - NOTICE: this does NOT check which object is above.

    Returns:
    - True if the following conditions are met:
        1. The objects are in contact with each other (checked by `check_contact`).
        2. The objects are horizontally aligned within a threshold (xy_threshold).
        3. The objects are vertically stacked within a defined gap range (z_min_gap to z_max_gap).
    - False otherwise.
    """
    def __call__(self, arg1, arg2):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]

        xy_threshold = 0.02
        z_min_gap = 0.001
        z_max_gap = 0.5

        horizontally_aligned = (
            abs(pos1[0] - pos2[0]) < xy_threshold
            and abs(pos1[1] - pos2[1]) < xy_threshold
        )

        vertical_stack = (
            z_min_gap < abs(pos1[2] - pos2[2]) < z_max_gap
        )

        return (
            arg1.check_contact(arg2)
            and horizontally_aligned
            and vertical_stack
        )

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class PrintJointState(UnaryAtomic):
    def __call__(self, arg):
        print(arg.get_joint_state())
        return True

    def expected_arg_types(self):
        return [BaseObjectState]


class Open(UnaryAtomic):
    def __call__(self, arg):
        return arg.is_open()

    def expected_arg_types(self):
        return [BaseObjectState]


class Close(UnaryAtomic):
    def __call__(self, arg):
        return arg.is_close()

    def expected_arg_types(self):
        return [BaseObjectState]

class OpenRatio(UnaryAtomic):
    """
    Check if the drawer's open ratio is within a specified tolerance from the expected open ratio.

    Usage: OpenRatio()(object, exp_ratio)
    Arguments:
    - object: The drawer object which has an open_ratio() method.
    - exp_ratio: The expected open ratio (a float between 0 to 1) to compare against.

    Returns:
    - True if the drawer's open ratio is within a tolerance of the expected ratio.
    - False otherwise.
    """    
    def __call__(self, arg, exp_ratio):
        tol = 0.2
        if abs(arg.open_ratio() - exp_ratio) < tol:
            return True
        else:
            return False
    
    def expected_arg_types(self):
        return [BaseObjectState, float]


class StairCase(UnaryAtomic):
    """
    Check if the drawer's open ratio follows a "staircase" pattern, 
    where each successive drawer is more open than the previous one.

    Usage: StairCase()(object1, object2, object3)
    Arguments:
    - object1: The first drawer object.
    - object2: The second drawer object.
    - object3: The third drawer object.

    Returns:
    - True if the open ratios follow an increasing pattern where:
        1. The first drawer's open ratio is greater than 0.1.
        2. The second drawer is more open than the first.
        3. The third drawer is more open than the second.
    - False otherwise.
    """
    def __call__(self, arg1, arg2, arg3):
        open_range = 0.1
        if (arg1.open_ratio() > open_range) and (arg1.open_ratio() < arg2.open_ratio()) and (arg2.open_ratio() < arg3.open_ratio()):
            return True
        else:
            return False
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState]
    
class InAir(UnaryAtomic):
    """
    Check if an object is above a specified height threshold (i.e., in the air).

    Usage: InAir()(object, height_threshold)
    Arguments:
    - object: The object to be checked for its height (must have a `get_geom_state()` method that returns its position).
    - height_threshold: The height (float) above which the object is considered to be "in the air".

    Returns:
    - True if the object's height is greater than the specified height threshold.
    - False otherwise.
    """
    def __call__(self, arg1, height_threshold):
        height = arg1.get_geom_state()["pos"][2]
        if height > height_threshold:
            return True
        else:
            return False
    
    def expected_arg_types(self):
        return [BaseObjectState, float]

class TurnOn(UnaryAtomic):
    def __call__(self, arg):
        return arg.turn_on()

    def expected_arg_types(self):
        return [BaseObjectState]


class TurnOff(UnaryAtomic):
    def __call__(self, arg):
        return arg.turn_off()

    def expected_arg_types(self):
        return [BaseObjectState]

class OnCentre(BinaryAtomic):
    '''
        Check whether an object is in the centre of another object with a margin of error.

        Usage: OnCentre()(object1, object2)
        Arguments:
        - arg1: The object that is supposed to be in the centre ontop of the second object (arg2).
        - arg2: The object that is supposed to be in the centre below the first object (arg1).
        
        Returns:
        - True if the object1 is ontop of object2 and is also in the centre of object2 within a margin of error of 0.005.
        - False otherwise.
            
    '''
    def check_ontop(self, arg2, arg1):
        this_object = arg2.env.get_object(arg2.object_name)
        this_object_position = arg2.env.sim.data.body_xpos[
            arg2.env.obj_body_id[arg2.object_name]
        ]
        other_object = arg2.env.get_object(arg1.object_name)
        other_object_position = arg2.env.sim.data.body_xpos[
            arg2.env.obj_body_id[arg1.object_name]
        ]
        return (
            (this_object_position[2] <= other_object_position[2])
            and arg2.check_contact(arg1)
            and (
                np.linalg.norm(this_object_position[:2] - other_object_position[:2])
                < 0.005
            )
        )
      
    def __call__(self, arg1, arg2):
        return self.check_ontop(arg2, arg1) 
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]




class Above(BinaryAtomic):
    """Check if arg1 is above arg2 in the z-axis, with a small xy threshold."""

    def __call__(self, arg1, arg2):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]
        xy_threshold = 0.02
        return (
            abs(pos1[0] - pos2[0]) < xy_threshold
            and abs(pos1[1] - pos2[1]) < xy_threshold
            and pos1[2] > pos2[2]
        )


class MidBetween(MultiarayAtomic):
    """Check if M is between L and R along axis A."""

    def __call__(self, L, M, R, A):
        assert A in {"x", "y", "z"}, "Axis must be one of 'x', 'y', or 'z'"
        pos_L = L.get_geom_state()["pos"]
        pos_M = M.get_geom_state()["pos"]
        pos_R = R.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[A]
        
        return (
            (
                (pos_L[axis_index] < pos_M[axis_index] < pos_R[axis_index])
                or (pos_R[axis_index] < pos_M[axis_index] < pos_L[axis_index])
            )
            and L.check_contact(M)
            and M.check_contact(R)
        )
