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
    """A predicate function that always returns True.

    Args:
        None
    Returns:
        bool: Always returns True.
    """
    def __init__(self):
        super().__init__()

    def __call__(self, *args):
        return True

    def expected_arg_types(self):
        return []


class FalsePredicateFn(MultiarayAtomic):
    """A predicate function that always returns False.
    Args:
        None
    Returns:
        bool: Always returns False.
    """
    def __init__(self):
        super().__init__()

    def __call__(self, *args):
        return False

    def expected_arg_types(self):
        return []


class Not(UnaryAtomic):
    """
    Logical NOT operation.
    Expects a single boolean input and returns its logical negation.
    
    Args:
        arg: A boolean value to negate.
    Returns:
        bool: The negation of the input boolean value.
    """
    def __call__(self, arg):
        return not arg

    def expected_arg_types(self):
        return [bool]


class And(BinaryAtomic):
    """
    Logical AND operation.
    Takes two boolean inputs and returns True if both are True.
    
    Args:
        arg1: First boolean value.
        arg2: Second boolean value.
    Returns:
        bool: True if both arg1 and arg2 are True, otherwise False.
    """
    def __call__(self, arg1, arg2):
        return arg1 and arg2

    def expected_arg_types(self):
        return [bool, bool]


class Or(BinaryAtomic):
    """
    Logical OR operation.
    Takes two boolean inputs and returns True if at least one is True.
    
    Args:
        arg1: First boolean value.
        arg2: Second boolean value.
    Returns:
        bool: True if either arg1 or arg2 is True, otherwise False.
    """
    def __call__(self, arg1, arg2):
        return arg1 or arg2

    def expected_arg_types(self):
        return [bool, bool]


class Any(UnaryAtomic):
    """
    Returns True if any element in the input tuple of booleans is True.
    Expects a tuple of booleans.
    
    Args:
        arg: A tuple of boolean values.
    Returns:
        bool: True if any element in the tuple is True, otherwise False.
    """
    def __call__(self, arg):
        if not isinstance(arg, tuple):
            raise TypeError("Any expects a tuple of booleans")
        return any(arg)

    def expected_arg_types(self):
        return [tuple]


class All(UnaryAtomic):
    """
    Returns True only if all elements in the input tuple of booleans are True.
    Expects a tuple of booleans.
    
    Args:
        arg: A tuple of boolean values.
    Returns:
        bool: True if all elements in the tuple are True, otherwise False.
    """
    def __call__(self, arg):
        if not isinstance(arg, tuple):
            raise TypeError("All expects a list or tuple of booleans")
        return all(arg)

    def expected_arg_types(self):
        return [tuple]

class Equal(BinaryAtomic):
    """
    Checks if two float values are approximately equal within a given threshold.
    Returns True if abs(arg1 - arg2) <= threshold.
    
    Args:
        arg1: First float value.
        arg2: Second float value.
        threshold: A float value representing the maximum allowable difference.
    Returns:
        bool: True if the absolute difference between arg1 and arg2 is within the threshold, otherwise False.
    """
    def __call__(self, arg1, arg2, threshold):
        return abs(arg1 - arg2) <= threshold

    def expected_arg_types(self):
        return [float, float, float]

class Minus(BinaryAtomic):
    """
    Subtracts the second float value from the first float value.
    Args:
        arg1: First float value.
        arg2: Second float value.
    Returns:
        float: The result of arg1 - arg2.    
    """
    def __call__(self, arg1, arg2):
        return arg1 - arg2

    def expected_arg_types(self):
        return [float, float]

class GreaterThan(BinaryAtomic):
    """
    Checks if the first float value is greater than the second float value.
    
    Args:
        arg1: First float value.
        arg2: Second float value.
    Returns:
        bool: True if arg1 is greater than arg2, otherwise False.
    """
    def __call__(self, arg1, arg2):
        return arg1 > arg2

    def expected_arg_types(self):
        return [float, float]


class LessThan(BinaryAtomic):
    """
    Checks if the first float value is less than the second float value.
    
    Args:
        arg1: First float value.
        arg2: Second float value.
    Returns:
        bool: True if arg1 is less than arg2, otherwise False.
    """
    def __call__(self, arg1, arg2):
        return arg1 < arg2

    def expected_arg_types(self):
        return [float, float]

class Arithmetic(MultiarayAtomic):
    """
    Perform a chain of arithmetic operations on a list of floats and operations.
    
    Usage: Arithmetic()(start_value, op1, val1, op2, val2, ...)
    Example: Arithmetic()(1.0, 'add', 2.0, 'subtract', 3.0)
    """
    def __call__(self, *args):
        if len(args) < 3 or len(args) % 2 == 0:
            raise ValueError("Expected at least one operation: (start_val, op1, val1, ...), with odd total length.")

        result = args[0]  # starting number
        i = 1
        while i < len(args):
            op = args[i]
            val = args[i + 1]

            if op == "add":
                result += val
            elif op == "subtract":
                result -= val
            elif op == "multiply":
                result *= val
            elif op == "divide":
                result /= val
            else:
                raise ValueError(f"Unsupported operation: {op}")
            i += 2
        return result

    def expected_arg_types(self, *args):
        return [float, str, float]
    
class TriangleCenter(BinaryAtomic):
    """
    Check if the position of arg1 is within a triangle defined by the positions of arg2, arg3, and arg4 on the XY plane.

    Args:
        arg1: The object whose position is being checked (BaseObjectState).
        arg2: The first vertex of the triangle (BaseObjectState).
        arg3: The second vertex of the triangle (BaseObjectState).
        arg4: The third vertex of the triangle (BaseObjectState).
    Returns:
        bool: True if arg1's position is within the triangle formed by arg2, arg3, and arg4, False otherwise.
    """
    def __call__(self, arg1, arg2, arg3, arg4, tol):
        pos1 = np.array(arg1.get_geom_state()["pos"])
        pos2 = np.array(arg2.get_geom_state()["pos"])
        pos3 = np.array(arg3.get_geom_state()["pos"])
        pos4 = np.array(arg4.get_geom_state()["pos"])

        # Project the positions onto the XY plane
        pos1_xy = pos1[:2]
        pos2_xy = pos2[:2]
        pos3_xy = pos3[:2]
        pos4_xy = pos4[:2]

        tolerance = tol # Tolerance for proximity check
        # Calculate the position of centroid of the triangle formed by pos2, pos3, and pos4
        centroid = (pos2_xy + pos3_xy + pos4_xy) / 3.0

        # check if pos1_xy is within the triangle formed by pos2_xy, pos3_xy, and pos4_xy
        return np.all(np.abs(pos1_xy - centroid) < tolerance)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState, BaseObjectState, float]


class Distance(BinaryAtomic):
    """
    Computes the Euclidean distance between two objects using their position data.
    
    Args:
        arg1: The first object (BaseObjectState) whose position is used.
        arg2: The second object (BaseObjectState) whose position is used.
    Returns:
        float: The Euclidean distance between the positions of arg1 and arg2.
    """
    def __call__(self, arg1, arg2):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]
        # print(np.linalg.norm(np.array(pos1) - np.array(pos2)))
        return np.linalg.norm(np.array(pos1) - np.array(pos2))

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]
    
class PlanarDistance(BinaryAtomic):
    """
    Computes the planar distance (ignoring the z-axis) between two objects using their position data.
    
    Args:
        arg1: The first object (BaseObjectState) whose position is used.
        arg2: The second object (BaseObjectState) whose position is used.
    Returns:
        float: The planar distance between the positions of arg1 and arg2.
    """
    def __call__(self, arg1, arg2):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]
        return np.linalg.norm(np.array(pos1[:2]) - np.array(pos2[:2]))

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]
    

class GetPosi(UnaryAtomic):
    """
    Retrieves a specific coordinate (x, y, or z) from an object's position.
    
    Usage: GetPosi()(object, axis)
    Args:
        arg: The object from which to retrieve the position.
        axis: A string indicating the axis ('x', 'y', or 'z') to retrieve.
    Returns:
        float: The position coordinate along the specified axis.
    """
    def __call__(self, arg, axis):
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")
        
        pos = arg.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        return pos[axis_index]

    def expected_arg_types(self):
        return [BaseObjectState, str]


class InContact(BinaryAtomic):
    """
    Check if two objects are in contact with each other.
    
    Usage: InContact()(object1, object2)
    Args:
        arg1: The first object to check for contact.
        arg2: The second object to check for contact.
    Returns:
        bool: True if arg1 and arg2 are in contact, False otherwise.
    """
    def __call__(self, arg1, arg2):
        return arg1.check_contact(arg2)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class In(BinaryAtomic):
    """
    Check if arg1 is contained within arg2.
    This predicate checks if the first object (arg1) is contained within the second object (arg2).
    
    Usage: In()(arg1, arg2)
    Args:
        arg1: The object to check for containment.
        arg2: The object that is expected to contain arg1.
    Returns:
        bool: True if arg1 is contained within arg2, False otherwise.
    """
    def __call__(self, arg1, arg2):
        return arg2.check_contact(arg1) and arg2.check_contain(arg1)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class On(BinaryAtomic):
    """
    With 3cm center alignement constraint (original)
    Check if arg1 is on top of arg2.
    This predicate checks if the first object (arg1) is on top of the second object (arg2),
    with a center alignment constraint of 3cm.
    
    Usage: On()(arg1, arg2)
    Args:
        arg1: The object expected to be on top.
        arg2: The object expected to be underneath.
    Returns:
        bool: True if arg1 is on top of arg2, False otherwise.
    """
    def __call__(self, arg1, arg2):
        return arg2.check_ontop(arg1)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]

class RelaxedOn(BinaryAtomic):
    """
    Without center alignment constraint
    Check if arg1 is on top of arg2.
    This predicate checks if the first object (arg1) is on top of the second object (arg2),
    without any center alignment constraint.
    
    Usage: RelaxedOn()(arg1, arg2)
    Args:
        arg1: The object expected to be on top.
        arg2: The object expected to be underneath.
    Returns:
        bool: True if arg1 is on top of arg2, False otherwise.
    """
    def __call__(self, arg1, arg2):
        return arg2.check_ontop(arg1, threshold=float('inf'))

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class PositionWithin(UnaryAtomic):
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
    def __call__(self, arg, pos_x, pos_y, pos_z, t_x, t_y, t_z):
        geom = arg.get_geom_state()
        pos = geom["pos"]
        # Check if the position is within the specified threshold
        within_x = abs(pos[0] - pos_x) <= t_x
        within_y = abs(pos[1] - pos_y) <= t_y
        within_z = abs(pos[2] - pos_z) <= t_z
        
        # print current position, target position, and threshold
        # position = (pos_x, pos_y, pos_z)
        # threshold = (t_x, t_y, t_z)
        # print(f"Current Position: {pos}, Target Position: {position}, Threshold: {threshold}")
        # print(f"Within X: {within_x}, Within Y: {within_y}, Within Z: {within_z}")
        return within_x and within_y and within_z
    
    def expected_arg_types(self):
        return [BaseObjectState, float, float, float, float, float, float]

class PositionWithinObject(UnaryAtomic):
    """
    Check if the position of one object is within a bounding box relative to another object's position.
    
    The method calculates the relative position difference between two objects (arg1 and arg2), and checks
    if that difference falls within the specified minimum and maximum bounds along each axis.
    
    This can be useful to determine whether one object is "near" or "inside" a region defined relative to another.

    Args:
        arg1: The object whose position is being checked.
        arg2: The reference object to define the bounding region.
        min_x, min_y, min_z: Minimum allowable differences in position (arg1 - arg2) along each axis.
        max_x, max_y, max_z: Maximum allowable differences in position (arg1 - arg2) along each axis.

    Returns:
        bool: True if arg1's position is within the specified bounds relative to arg2, False otherwise.
    """
    def __call__(self, arg1, arg2, min_x, min_y, min_z, max_x, max_y, max_z):
        geom1 = arg1.get_geom_state()
        geom2 = arg2.get_geom_state()
        pos1 = geom1["pos"]
        pos2 = geom2["pos"]
        # Check if the position is within the specified threshold
        within_x = min_x <= pos1[0] - pos2[0] <= max_x
        within_y = min_y <= pos1[1] - pos2[1] <= max_y
        within_z = min_z <= pos1[2] - pos2[2] <= max_z

        # print(f"x difference: {pos1[0] - pos2[0]}, y difference: {pos1[1] - pos2[1]}, z difference: {pos1[2] - pos2[2]}")
        # print(f"Within X: {within_x}, Within Y: {within_y}, Within Z: {within_z}")
        return within_x and within_y and within_z
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, float, float, float, float, float, float]

class Under(BinaryAtomic):
    """
    Check if arg1 is under arg2 in the z-axis, with a small xy threshold.
    This predicate checks if the first object (arg1) is under the second object (arg2),
    with a center alignment constraint of 2cm in the x and y axes.
    
    Usage: Under()(arg1, arg2)
    Args:
        arg1: The object expected to be under.
        arg2: The object expected to be above.
    Returns:
        bool: True if arg1 is under arg2, False otherwise.
    """
    def __call__(self, arg1, arg2):
        return arg1.get_geom_state()["pos"][2] <= arg2.get_geom_state()["pos"][2]

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]


class Up(UnaryAtomic):
    """
    Check if the object is above a certain height threshold.
    This predicate checks if the z-coordinate of the object's position is greater than or equal to 1.0.
    
    Usage: Up()(arg1)
    Args:
        arg1: The object to check.
    Returns:
        bool: True if the object's z-coordinate is greater than or equal to 1.0, False otherwise.
    """
    def __call__(self, arg1):
        return arg1.get_geom_state()["pos"][2] >= 1.0

    def expected_arg_types(self):
        return [BaseObjectState]


class UpsideDown(UnaryAtomic):
    """
    Check if the object is upside down based on its quaternion orientation.
    This predicate checks if the z-axis of the object's orientation is pointing downwards,
    which is determined by the z-component of the quaternion being less than -0.95.
    
    Usage: UpsideDown()(arg1)
    Args:
        arg1: The object to check.
    Returns:
        bool: True if the object is upside down (z-axis pointing downwards), False otherwise.
    """
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
    """
    Check if the object is upright based on its quaternion orientation.
    This predicate checks if the z-axis of the object's orientation is pointing upwards,
    which is determined by the z-component of the quaternion being greater than or equal to 0.9.
    Usage: Upright()(arg1)
    Args:
        arg: The object to check.
    Returns:
        bool: True if the object is upright (z-axis pointing upwards), False otherwise.
    """
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
    """
    Check if the object's position is greater than a specified value along a specified axis.
    
    Usage: PosiGreaterThan()(object, axis, value)
    Args:
        arg: The object whose position is being checked.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        value: A float value to compare against the object's position along the specified axis.
    Returns:
        bool: True if the object's position along the specified axis is greater than the given value, False otherwise.
    """
    def __call__(self, *args):
        arg, axis, value = args
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")

        pos = arg.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        return pos[axis_index] > value
    
    def expected_arg_types(self):
        return [BaseObjectState, str, float]

class PosiGreaterThanObject(UnaryAtomic):
    """
    Check if the position of one object is greater than another object's position along a specified axis with an offset.
    Usage: PosiGreaterThanObject()(object1, object2, axis, offset)
    Args:
        obj1: The first object whose position is being checked.
        obj2: The second object whose position is used for comparison.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        offset: A float value to add to the second object's position along the specified axis.
    Returns:
        bool: True if the position of obj1 along the specified axis is greater than the position of obj2 plus the offset, False otherwise.
    """
    def __call__(self, *args):
        obj1, obj2, axis, offset  = args
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")

        pos1 = obj1.get_geom_state()["pos"]
        pos2 = obj2.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        return pos1[axis_index] > (pos2[axis_index] + offset)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, str, float]
    
class PosiLessThan(UnaryAtomic):
    """
    Check if the object's position is less than a specified value along a specified axis.
    
    Usage: PosiLessThan()(object, axis, value)
    Args:
        arg: The object whose position is being checked.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        value: A float value to compare against the object's position along the specified axis.
    Returns:
        bool: True if the object's position along the specified axis is less than the given value, False otherwise.
    """
    def __call__(self, *args):
        arg, axis, value = args
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")

        pos = arg.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        return pos[axis_index] < value
    
    def expected_arg_types(self):
        return [BaseObjectState, str, float]

class PosiLessThanObject(UnaryAtomic):
    """
    Check if the position of one object is less than another object's position along a specified axis with an offset.
    
    Usage: PosiLessThanObject()(object1, object2, axis, offset)
    Args:
        obj1: The first object whose position is being checked.
        obj2: The second object whose position is used for comparison.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        offset: A float value to subtract from the second object's position along the specified axis.
    Returns:
        bool: True if the position of obj1 along the specified axis is less than the position of obj2 minus the offset, False otherwise.
    """
    def __call__(self, *args):
        obj1, obj2, axis, offset  = args
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")

        pos1 = obj1.get_geom_state()["pos"]
        pos2 = obj2.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        return pos1[axis_index] < (pos2[axis_index] - offset)

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, str, float]

class AxisAlignedWithin(UnaryAtomic):
    """
    Check if the object's specified axis is within a degree range [min_deg, max_deg]
    from alignment with the world Z+ axis.

    Usage: AxisAlignedWithin()(object, axis, min_deg, max_deg)
    Args:
        obj: The object whose orientation is being checked.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        min_deg: Minimum angle in degrees for the axis to be considered aligned.
        max_deg: Maximum angle in degrees for the axis to be considered aligned.
    Returns:
        bool: True if the object's specified axis is within the degree range from alignment with Z+,
        False otherwise.
    Raises:
        ValueError: If the axis is not one of 'x', 'y', or 'z', or if the degree range is invalid.
    """

    def __call__(self, *args):
        if len(args) != 4:
            raise ValueError("AxisAlignedWithin expects 4 arguments: object, axis ('x', 'y', 'z'), min_degree, max_degree")
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
        
        # this is used to print the current angle of the axis with respect to Z+ for debugging
        # calculate current angle in degrees
        # angle_rad = np.arccos(cos_angle)
        # angle_deg = np.degrees(angle_rad)
        # print(f"Current angle of {axis} axis with Z+ is {angle_deg:.2f} degrees")

        return cos_max <= cos_angle <= cos_min

    def expected_arg_types(self):
        return [BaseObjectState, str, float, float]
    
class AxisAlignedWithinWorldAxis(UnaryAtomic):
    """
    Check if the object's specified axis is within a degree range [min_deg, max_deg]
    from alignment with a reference axis in world coordinates.

    Usage: AxisAlignedWithin()(object, axis, min_deg, max_deg, reference_axis)
    Args:
        obj: The object whose orientation is being checked.
        axis: A string indicating the object's axis ('x', 'y', or 'z') to check.
        min_deg: Minimum angle in degrees for the axis to be considered aligned.
        max_deg: Maximum angle in degrees for the axis to be considered aligned.
        reference_axis: A string indicating the world reference axis ('x', 'y', or 'z') 
                       to measure against. Defaults to 'z' for backward compatibility.
    Returns:
        bool: True if the object's specified axis is within the degree range from 
              alignment with the reference axis, False otherwise.
    Raises:
        ValueError: If the axis or reference_axis is not one of 'x', 'y', or 'z', 
                   or if the degree range is invalid.
    """

    def __call__(self, obj, axis, min_deg, max_deg, reference_axis):
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")
        if reference_axis not in {"x", "y", "z"}:
            raise ValueError("Reference axis must be one of 'x', 'y', or 'z'")
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

        # Get the object's axis vector in world coordinates
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        object_axis_world = R[:, axis_index]
        
        # Get the reference axis vector in world coordinates
        reference_vectors = {
            "x": np.array([1.0, 0.0, 0.0]),
            "y": np.array([0.0, 1.0, 0.0]), 
            "z": np.array([0.0, 0.0, 1.0])
        }
        reference_vector = reference_vectors[reference_axis]
        
        # Calculate the cosine of the angle between the object axis and reference axis
        cos_angle = np.dot(object_axis_world, reference_vector)

        return cos_max <= cos_angle <= cos_min

    def expected_arg_types(self):
        return [BaseObjectState, str, float, float, str]

class AxisAlignedWithinY(UnaryAtomic):
    """
    Check if the object's specified axis is within a degree range [min_deg, max_deg]
    from alignment with the world Y+ axis.

    Usage: AxisAlignedWithinY()(object, min_deg, max_deg)
    Args:
        obj: The object whose orientation is being checked.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        min_deg: Minimum angle in degrees for the axis to be considered aligned.
        max_deg: Maximum angle in degrees for the axis to be considered aligned.
    Returns:
        bool: True if the object's specified axis is within the degree range from alignment with Z+,
        False otherwise.
    Raises:
        ValueError: If the axis is not one of 'x', 'y', or 'z', or if the degree range is invalid.
    """

    def __call__(self, *args):
        if len(args) != 4:
            raise ValueError("AxisAlignedWithinY expects 4 arguments: object, axis ('x', 'y', 'z'), min_degree, max_degree")
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
        cos_angle = object_axis_world[1]
        
        # # this is used to print the current angle of the axis with respect to Z+ for debugging
        # # calculate current angle in degrees
        # angle_rad = np.arccos(cos_angle)
        # angle_deg = np.degrees(angle_rad)
        # print(f"Current angle of {axis} axis with Z+ is {angle_deg:.2f} degrees")

        return cos_max <= cos_angle <= cos_min

    def expected_arg_types(self):
        return [BaseObjectState, str, float, float]

class AxisAlignedWithinY(UnaryAtomic):
    """
    Check if the object's specified axis is within a degree range [min_deg, max_deg]
    from alignment with the world Y+ axis.

    Usage: AxisAlignedWithinY()(object, min_deg, max_deg)
    Args:
        obj: The object whose orientation is being checked.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        min_deg: Minimum angle in degrees for the axis to be considered aligned.
        max_deg: Maximum angle in degrees for the axis to be considered aligned.
    Returns:
        bool: True if the object's specified axis is within the degree range from alignment with Z+,
        False otherwise.
    Raises:
        ValueError: If the axis is not one of 'x', 'y', or 'z', or if the degree range is invalid.
    """

    def __call__(self, *args):
        if len(args) != 4:
            raise ValueError("AxisAlignedWithinY expects 4 arguments: object, axis ('x', 'y', 'z'), min_degree, max_degree")
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
        cos_angle = object_axis_world[1]
        
        # # this is used to print the current angle of the axis with respect to Z+ for debugging
        # # calculate current angle in degrees
        # angle_rad = np.arccos(cos_angle)
        # angle_deg = np.degrees(angle_rad)
        # print(f"Current angle of {axis} axis with Z+ is {angle_deg:.2f} degrees")

        return cos_max <= cos_angle <= cos_min

    def expected_arg_types(self):
        return [BaseObjectState, str, float, float]

class PrintGeomState(UnaryAtomic):
    """
    Print the geometry state of an object at specified intervals.
    
    Usage: PrintGeomState()(object, interval)
    Args:
        object: The object whose geometry state will be printed.
    Returns:
        True: Always returns True, as this is a side-effect action.
    """
    def __init__(self):
        super().__init__()
        self.count = {}

    def __call__(self, arg, interval):
        if arg.object_name not in self.count:
            self.count[arg.object_name] = 0

        if self.count[arg.object_name] % interval == 0:
            geom_state = arg.get_geom_state()
            print(f"Geometry State of {arg.object_name}: {geom_state}")

        self.count[arg.object_name] += 1
        return True

    def expected_arg_types(self):
        return [BaseObjectState, int]

class StackBowl(BinaryAtomic):
    """
    Check if two objects are stacked on top of each other, ensuring that they are 
    horizontally aligned and vertically separated within a defined range.

    Usage: StackBowl()(object1, object2)
    Arguments:
        object1: The first object that needs to be checked for stacking.
        object2: The second object that needs to be checked for stacking.
    NOTICE: this does NOT check which object is above.

    Returns:
        True if the following conditions are met:
            1. The objects are in contact with each other (checked by `check_contact`).
            2. The objects are horizontally aligned within a threshold (xy_threshold).
            3. The objects are vertically stacked within a defined gap range (z_min_gap to z_max_gap).
        False otherwise.
    """
    def __call__(self, arg1, arg2):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]

        xy_threshold = 0.05
        z_min_gap = 0.001
        z_max_gap = 0.3

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
    """
    Print the joint state of an object.
    
    Usage: PrintJointState()(object)
    Arguments:
        object: The object whose joint state will be printed.
    Returns:
        True: Always returns True, as this is a side-effect action.
    """
    def __call__(self, arg):
        print(arg.get_joint_state())
        return True

    def expected_arg_types(self):
        return [BaseObjectState]


class Open(UnaryAtomic):
    """
    Check if the object is open.
    This predicate checks if the object is in an open state, which is typically defined by its joint positions.
    
    Usage: Open()(object)
    Args:
        arg: The object to check for an open state.
    Returns:
        bool: True if the object is open, False otherwise.
    """
    def __call__(self, arg):
        return arg.is_open()

    def expected_arg_types(self):
        return [BaseObjectState]


class Close(UnaryAtomic):
    """
    Check if the object is closed.
    This predicate checks if the object is in a closed state, which is typically defined by its joint positions.
    
    Usage: Close()(object)
    Args:
        arg: The object to check for a closed state.
    Returns:
        bool: True if the object is closed, False otherwise.
    """
    def __call__(self, arg):
        return arg.is_close()

    def expected_arg_types(self):
        return [BaseObjectState]

class OpenRatio(UnaryAtomic):
    """
    Check if the drawer's open ratio is within a specified tolerance from the expected open ratio.

    Usage: OpenRatio()(object, exp_ratio)
    Arguments:
        object: The drawer object which has an open_ratio() method.
        exp_ratio: The expected open ratio (a float between 0 to 1) to compare against.

    Returns:
        True if the drawer's open ratio is within a tolerance of the expected ratio.
        False otherwise.
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
        object1: The first drawer object.
        object2: The second drawer object.
        object3: The third drawer object.

    Returns:
        True if the open ratios follow an increasing pattern where:
            1. The first drawer's open ratio is greater than 0.1.
            2. The second drawer is more open than the first.
            3. The third drawer is more open than the second.
        False otherwise.
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
        object: The object to be checked for its height (must have a `get_geom_state()` method that returns its position).
        height_threshold: The height (float) above which the object is considered to be "in the air".

    Returns:
        True if the object's height is greater than the specified height threshold.
        False otherwise.
    """
    def __call__(self, arg1, height_threshold):
        height = arg1.get_geom_state()["pos"][2]
        if height > height_threshold:
            return True
        else:
            return False
    
    def expected_arg_types(self):
        return [BaseObjectState, float]
    
class SameHeight(BinaryAtomic):
    """
    Check if two objects are at the same height within a small threshold.
    This predicate checks if the z-coordinates of the two objects' positions are within a small threshold (0.01).
    
    Usage: SameHeight()(object1, object2)
    Args:
        arg1: The first object to check.
        arg2: The second object to check.
    Returns:
        bool: True if the z-coordinates of arg1 and arg2 are within 0.01 of each other, False otherwise.
    """
    def __call__(self, arg1, arg2):
        return abs(arg1.get_geom_state()["pos"][2] - arg2.get_geom_state()["pos"][2]) < 0.01

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]

class TurnOn(UnaryAtomic):
    """
    Turn on an object, typically a light or a device.
    
    Usage: TurnOn()(object)
    Args:
        arg: The object to be turned on.
    Returns:
        The result of the turn_on method of the object.
    """
    def __call__(self, arg):
        return arg.turn_on()

    def expected_arg_types(self):
        return [BaseObjectState]


class TurnOff(UnaryAtomic):
    """
    Turn off an object, typically a light or a device.
    
    Usage: TurnOff()(object)
    Args:
        arg: The object to be turned off.
    Returns:
        The result of the turn_off method of the object.
    """
    def __call__(self, arg):
        return arg.turn_off()

    def expected_arg_types(self):
        return [BaseObjectState]

class Above(BinaryAtomic):
    """
    This predicate checks if the first object (arg1) is above the second object (arg2) but not necessarily in contact.,
    with a center alignment constraint of 2cm in the x and y axes.
    
    Usage: Above()(arg1, arg2)
    Args:
        arg1: The object expected to be above.
        arg2: The object expected to be below.
    Returns:
        bool: True if arg1 is above arg2, False otherwise.
    """

    def __call__(self, arg1, arg2):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]
        xy_threshold = 0.02
        return (
            abs(pos1[0] - pos2[0]) < xy_threshold
            and abs(pos1[1] - pos2[1]) < xy_threshold
            and pos1[2] > pos2[2]
        )

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState]

class FlexibleAbove(BinaryAtomic):
    """
    This predicate checks if the first object (arg1) is above the second object (arg2) but not necessarily in contact.,
    with a flexible center alignment constraint.
    
    Usage: Above()(arg1, arg2)
    Args:
        arg1: The object expected to be above.
        arg2: The object expected to be below.
        xy_threshold: Centre alignment thresholds.
    Returns:
        bool: True if arg1 is above arg2, False otherwise.
    """

    def __call__(self, arg1, arg2, xy_threshold):
        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]
        return (
            abs(pos1[0] - pos2[0]) < xy_threshold
            and abs(pos1[1] - pos2[1]) < xy_threshold
            and pos1[2] > pos2[2]
        )

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, float]

class MidBetween(MultiarayAtomic):
    """
    This predicate checks if the middle object (M) is positioned between the left object (L) and the right object (R)
    along a specified axis (A), and that both L and R are in contact with M.
    
    Usage: MidBetween()(L, M, R, A)
    Args:
        L: The left object (BaseObjectState).
        M: The middle object (BaseObjectState).
        R: The right object (BaseObjectState).
        A: A string indicating the axis ('x', 'y', or 'z') to check.
    Returns:
        bool: True if M is between L and R along axis A, and both L and R are in contact with M.
        False otherwise.
    """

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

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState, str]
    
class MidBetweenAnyDirection(MultiarayAtomic):
    """
    Checks if the middle object (M) is between the left object (L) and the right object (R)
    in any direction (not limited to a specific axis), by checking the angle between LM and MR vectors.

    Usage: MidBetweenAnyDirection()(L, M, R, ignore_z=True, angle_threshold=30)
    Args:
        L: The first object (BaseObjectState).
        M: The middle object (BaseObjectState).
        R: The third object (BaseObjectState).
        ignore_z: If True, only consider the xy plane.
        angle_threshold: The maximum angle (in degrees) allowed between LM and MR (suggested: 30).
    Returns:
        bool: True if the angle between LM and MR is less than angle_threshold degrees,
              and L is in contact with M, and M is in contact with R.
    """
    def __call__(self, L, M, R, ignore_z=True, angle_threshold=30):
        pos_L = np.array(L.get_geom_state()["pos"])
        pos_M = np.array(M.get_geom_state()["pos"])
        pos_R = np.array(R.get_geom_state()["pos"])

        if ignore_z:
            pos_L = pos_L[:2]
            pos_M = pos_M[:2]
            pos_R = pos_R[:2]

        v_LM = pos_M - pos_L
        v_MR = pos_R - pos_M

        norm_LM = np.linalg.norm(v_LM)
        norm_MR = np.linalg.norm(v_MR)
        if norm_LM == 0 or norm_MR == 0:
            return False  # Avoid division by zero

        cos_angle = np.dot(v_LM, v_MR) / (norm_LM * norm_MR)
        # Clamp to [-1, 1] to avoid numerical issues
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        # Convert angle_threshold to cosine
        angle_threshold_rad = np.radians(angle_threshold)
        cos_threshold = np.cos(angle_threshold_rad)

        return (
            cos_angle > cos_threshold
            and L.check_contact(M)
            and M.check_contact(R)
        )

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState, bool, float]
    
class RelaxedMidBetween(MultiarayAtomic):
    """
    Check if M is between L and R along axis A without contact requirement.
    
    Usage: RelaxedMidBetween()(L, M, R, A)
    Args:
        L: The left object (BaseObjectState).
        M: The middle object (BaseObjectState).
        R: The right object (BaseObjectState).
        A: A string indicating the axis ('x', 'y', or 'z') to check.
    Returns:
        bool: True if M is between L and R along axis A, False otherwise.
    """

    def __call__(self, L, M, R, A):
        assert A in {"x", "y", "z"}, "Axis must be one of 'x', 'y', or 'z'"
        pos_L = L.get_geom_state()["pos"]
        pos_M = M.get_geom_state()["pos"]
        pos_R = R.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[A]
        
        # print current positions for debugging
        # print(f"Position L: {pos_L}, Position M: {pos_M}, Position R: {pos_R}")
        
        return (
            (pos_L[axis_index] < pos_M[axis_index] < pos_R[axis_index])
            or (pos_R[axis_index] < pos_M[axis_index] < pos_L[axis_index])
        )

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState, str]

    
class Linear(MultiarayAtomic):
    """
    Check if three objects L, M, and R are collinear in the x-y plane.
    This predicate checks if the area of the triangle formed by the positions of L, M, and R is less than a specified tolerance.
    
    Usage: Linear()(L, M, R, tolerance)
    Args:
        L: The left object (BaseObjectState).
        M: The middle object (BaseObjectState).
        R: The right object (BaseObjectState).
        tolerance: A float value representing the tolerance for collinearity.
    Returns:
        bool: True if L, M, and R are collinear within the specified tolerance, False otherwise.
    """
    def __call__(self, L, M, R, tolerance):
        x1, y1, z1 = L.get_geom_state()["pos"]
        x2, y2, z2 = M.get_geom_state()["pos"]
        x3, y3, z3 = R.get_geom_state()["pos"]
        
        # Calculate the area of the triangle formed by x_i,y_i
        area = 0.5 * abs(
            x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        )
        # If the area is close to zero, the points are collinear
        return area < tolerance
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState, float]
    
class LROrdering(MultiarayAtomic):
    """
    This predicate checks if a sequence of objects is ordered from left to right based on their y-coordinates.
    
    Usage: LROrdering()(object1, object2, object3)
    Args:
        *args: Three BaseObjectState objects to be checked for left-to-right ordering.
    Returns:
        bool: True if the objects are ordered from left to right based on their y-coordinates, False otherwise.
    """
    
    def __call__(self, *args):
        assert len(args) >= 2, "At least two objects are required for ordering"
        for i in range(len(args) - 1):
            pos1 = args[i].get_geom_state()["pos"]
            pos2 = args[i + 1].get_geom_state()["pos"]
            if pos1[1] >= pos2[1]:
                return False
        return True
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState]


class OrderAlongAxis(MultiarayAtomic):
    """
    Check if a sequence of objects is ordered along a specified axis (x, y, or z).
    
    Usage: OrderAlongAxis()(axis, object1, object2, ..., objectN)
    Args:
        axis: A string indicating the axis ('x', 'y', or 'z') to check for ordering.
        *args: A variable number of BaseObjectState objects to be checked for ordering along the specified axis.
    Returns:
        bool: True if the objects are ordered along the specified axis, False otherwise.
    """
    
    def __call__(self, axis, *args):
        assert axis in {"x", "y", "z"}, "Axis must be one of 'x', 'y', or 'z'"
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        
        for i in range(len(args) - 1):
            pos1 = args[i].get_geom_state()["pos"]
            pos2 = args[i + 1].get_geom_state()["pos"]
            if pos1[axis_index] >= pos2[axis_index]:
                return False
        return True
    
    def expected_arg_types(self):
        return [str] + [BaseObjectState] * 3  # Adjust the number of BaseObjectState as needed


class DistanceBetween(BinaryAtomic):
    """
    Check whether an object is close to another object with a user-defined margin of error for x,y,z separately.

    Usage: DistanceBetween()(object1, object2, x, y, z)
    Arguments:
        arg1: The object that is supposed to be in the centre ontop of the second object (arg2).
        arg2: The object that is supposed to be in the centre below the first object (arg1).
        (x,y,z): The thresholds
    
    Returns:
        True if the objects are close to each other within the user-defined margin of error.
        False otherwise.
    """
    def check_centre(self, arg2, arg1, x, y, z):
        this_object = arg2.env.get_object(arg2.object_name)
        this_object_position = arg2.env.sim.data.body_xpos[
            arg2.env.obj_body_id[arg2.object_name]
        ]
        other_object = arg2.env.get_object(arg1.object_name)
        other_object_position = arg2.env.sim.data.body_xpos[
            arg2.env.obj_body_id[arg1.object_name]
        ]
        
        return ( 
            (np.linalg.norm(this_object_position[:1] - other_object_position[:1])
                < x
            ) and (
                np.linalg.norm(this_object_position[1:2] - other_object_position[1:2])
                < y
            ) and (
                np.linalg.norm(this_object_position[2:] - other_object_position[2:]) < z)
            )
      
    def __call__(self, arg1, arg2, x, y, z):
        return self.check_centre(arg2, arg1, x, y ,z)
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, float, float, float]
    
class FlexibleOn(BinaryAtomic):
    """
    Check whether an object is on the centre of another object with a flexible margin of error for x,y separately.

    Usage: FlexibleOn()(object1, object2, x, y)
    Arguments:
        arg1: The object that is supposed to be in the centre ontop of the second object (arg2).
        arg2: The object that is supposed to be in the centre below the first object (arg1).
        (x,y): The thresholds
    Returns:
        True if the object1 is on the centre of object2 within the user-defined margin of error.
        False otherwise.
    """
    def check_centre(self, arg2, arg1, x, y):
        this_object = arg2.env.get_object(arg2.object_name)
        this_object_position = arg2.env.sim.data.body_xpos[
            arg2.env.obj_body_id[arg2.object_name]
        ]
        other_object = arg2.env.get_object(arg1.object_name)
        other_object_position = arg2.env.sim.data.body_xpos[
            arg2.env.obj_body_id[arg1.object_name]
        ]
        
        return (
            arg2.check_contact(arg1)
            and (
                np.linalg.norm(this_object_position[:1] - other_object_position[:1])
                < x
            ) and (
                np.linalg.norm(this_object_position[1:2] - other_object_position[1:2])
                < y
            ) and (
                this_object_position[2] <= other_object_position[2])
            )
      
    def __call__(self, arg1, arg2, x, y):
        return self.check_centre(arg2, arg1, x, y) 
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, float, float]

class OrientedAtDegree(UnaryAtomic):
    """
    Check if the object's orientation (roll, pitch, yaw) is within the specified degree thresholds.

    Usage: OrientedAtDegree()(object, roll, pitch, yaw, roll_thresh, pitch_thresh, yaw_thresh)
    Arguments:
    - object: The object to check.
    - roll, pitch, yaw: Target euler angles in degrees.
    - roll_thresh, pitch_thresh, yaw_thresh: Allowed deviation for each angle in degrees.

    Returns:
    - True if all angles are within their respective thresholds.
    """
    def __call__(self, arg, roll, pitch, yaw, roll_thresh, pitch_thresh, yaw_thresh):
        geom = arg.get_geom_state()
        w, x, y, z = geom["quat"]
        quat = np.array([x, y, z, w])
        R = transform_utils.quat2mat(quat)
        roll_curr, pitch_curr, yaw_curr = transform_utils.mat2euler(R)
        # Convert to degrees
        roll_curr = np.degrees(roll_curr)
        pitch_curr = np.degrees(pitch_curr)
        yaw_curr = np.degrees(yaw_curr)
        
        def acute_diff(a, b):
            diff = abs(a - b)
            if diff > 180:
                diff = 360 - diff
            return diff

        within_roll = acute_diff(roll_curr, roll) <= roll_thresh
        within_pitch = acute_diff(pitch_curr, pitch) <= pitch_thresh
        within_yaw = acute_diff(yaw_curr, yaw) <= yaw_thresh
        return within_roll and within_pitch and within_yaw

    def expected_arg_types(self):
        return [BaseObjectState, float, float, float, float, float, float]

class GetOrientation(UnaryAtomic):
    """
    Get the orientation of the object in the specified format.
    
    Args:
        arg: The object whose orientation is being checked.
        orient: The type of orientation to return ('roll', 'pitch', or 'yaw').
    
    Returns:
        float or np.array: The orientation value(s) in the specified format.
    """
    def __call__(self, arg, type):
        geom = arg.get_geom_state()
        w, x, y, z = geom["quat"]
        quat = np.array([x, y, z, w])
        R = transform_utils.quat2mat(quat)
        
        if type == "roll":
            return np.degrees(transform_utils.mat2euler(R)[0])
        elif type == "pitch":
            return np.degrees(transform_utils.mat2euler(R)[1])
        elif type == "yaw":
            return np.degrees(transform_utils.mat2euler(R)[2])
        else:
            raise ValueError("Invalid orientation type. Choose from 'roll', 'pitch', 'yaw'.")
    
    def expected_arg_types(self):
        return [BaseObjectState, str]


class PositionWithinObjectAnnulus(UnaryAtomic):
    """
    Check if the position of one object is within a bounding annulus relative to another object's position in the x-y plane.

    Usage: PositionWithinObjectAnnulus()(arg1, arg2, min_radius, max_radius)
    Args:
        arg1: The object whose position is being checked.
        arg2: The reference object to define the bounding region.
        min_radius: The minimum distance from arg2's position.
        max_radius: The maximum distance from arg2's position.
    Returns:
        bool: True if arg1's position is within the specified bounds relative to arg2, False otherwise.
    """
    def __call__(self, arg1, arg2, min_radius, max_radius):
        if min_radius < 0 or max_radius < 0:
            raise ValueError("min_radius and max_radius must be non-negative")
        geom1 = arg1.get_geom_state()
        geom2 = arg2.get_geom_state()
        pos1 = geom1["pos"]
        pos2 = geom2["pos"]

        # Check if the position is within the annulus defined by min_radius and max_radius
        distance = np.linalg.norm(np.array(pos1[:2]) - np.array(pos2[:2]))
        within_radius = min_radius <= distance <= max_radius

        # print(f"Distance: {distance}, Min Radius: {min_radius}, Max Radius: {max_radius}, Within Radius: {within_radius}")
        return within_radius

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, float, float]
    
# class Stack(BinaryAtomic):
#     def __call__(self, arg1, arg2):
#         return (
#             arg1.check_contact(arg2)
#             and arg2.check_contain(arg1)
#             and arg1.get_geom_state()["pos"][2] > arg2.get_geom_state()["pos"][2]
#         )

#     def expected_arg_types(self):
#         return [BaseObjectState, BaseObjectState]


class RightAngle(MultiarayAtomic):
    """
    Check if three objects form a right angle (90 degrees) with the middle object at the corner.
    This predicate checks if the angle formed by the vectors from the corner object to the other two objects
    is close to 90 degrees within a specified tolerance.
    
    Usage: RightAngle()(corner_object, object1, object2, tolerance_degrees)
    Args:
        corner_object: The object at the corner of the right angle (BaseObjectState).
        object1: The first object forming one arm of the angle (BaseObjectState).
        object2: The second object forming the other arm of the angle (BaseObjectState).
        tolerance_degrees: The tolerance in degrees for the right angle check (float).
    Returns:
        bool: True if the angle is within tolerance_degrees of 90 degrees, False otherwise.
    """
    def __call__(self, corner_object, object1, object2, tolerance_degrees):
        # Get positions in x-y plane (ignoring z for 2D angle calculation)
        corner_pos = corner_object.get_geom_state()["pos"]
        pos1 = object1.get_geom_state()["pos"]
        pos2 = object2.get_geom_state()["pos"]
        
        # Create vectors from corner to each object (in x-y plane)
        vec1 = np.array([pos1[0] - corner_pos[0], pos1[1] - corner_pos[1]])
        vec2 = np.array([pos2[0] - corner_pos[0], pos2[1] - corner_pos[1]])
        
        # Calculate magnitudes
        mag1 = np.linalg.norm(vec1)
        mag2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if mag1 < 1e-6 or mag2 < 1e-6:
            return False
        
        # Normalize vectors
        vec1_norm = vec1 / mag1
        vec2_norm = vec2 / mag2
        
        # Calculate dot product
        dot_product = np.dot(vec1_norm, vec2_norm)
        
        # Clamp dot product to avoid numerical errors in arccos
        dot_product = np.clip(dot_product, -1.0, 1.0)
        
        # Calculate angle in degrees
        angle_rad = np.arccos(dot_product)
        angle_deg = np.degrees(angle_rad)
        
        # Check if angle is within tolerance of 90 degrees
        return abs(angle_deg - 90.0) <= tolerance_degrees
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState, float]

class OppositeSides(MultiarayAtomic):
    """
    Check if two objects are positioned on opposite sides of a third object (the divider).
    This predicate checks if the divider object is between the two other objects along any axis,
    indicating they are on opposite sides.
    
    Usage: OppositeSides()(object1, object2, divider_object)
    Args:
        object1: The first object (BaseObjectState).
        object2: The second object (BaseObjectState).
        divider_object: The object that should be between object1 and object2 (BaseObjectState).
    Returns:
        bool: True if the divider is between object1 and object2 along at least one axis, False otherwise.
    """
    def __call__(self, object1, object2, divider_object):
        pos1 = object1.get_geom_state()["pos"]
        pos2 = object2.get_geom_state()["pos"]
        divider_pos = divider_object.get_geom_state()["pos"]
        
        # Check if divider is between object1 and object2 along any axis (x, y, or z)
        for axis in range(3):  # x=0, y=1, z=2
            # Check if divider position is between the two objects on this axis
            if ((pos1[axis] <= divider_pos[axis] <= pos2[axis]) or 
                (pos2[axis] <= divider_pos[axis] <= pos1[axis])):
                # Also ensure the objects are actually separated (not at the same position)
                if abs(pos1[axis] - pos2[axis]) > 0.01:  # minimum separation threshold
                    return True
        
        return False
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, BaseObjectState]


class NeuralJudge(MultiarayAtomic):
    def __init__(self):
        super().__init__()

    def __call__(self, *args):
        return False

    def expected_arg_types(self):
        return [str]

    
class PosiSameWith(BinaryAtomic):
    """
    Check if the position of an object is the same as another object within a specified threshold.
    Usage: PosiSameWith()(arg1, arg2, axis, threshold)
    Args:
        arg1: The first object whose position is being checked.
        arg2: The second object to compare against.
        axis: A string indicating the axis ('x', 'y', or 'z') to check.
        threshold: A float value representing the maximum allowable difference in position along the specified axis.
    Returns:
        bool: True if the position of arg1 along the specified axis is within the threshold of arg2's position, False otherwise.
    """
    def __call__(self, arg1, arg2, axis, threshold):
        if axis not in {"x", "y", "z"}:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")

        pos1 = arg1.get_geom_state()["pos"]
        pos2 = arg2.get_geom_state()["pos"]
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        
        return abs(pos1[axis_index] - pos2[axis_index]) <= threshold
    
    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, str, float]

class IsTouchingSideAxis(BinaryAtomic):
    """
    Checks if one object (arg1) is touching another object (arg2) along a specified local axis ('x', 'y', or 'z').

    It verifies:
    1. The two objects are in physical contact.
    2. The vector from arg2's center to arg1's center is aligned with arg2's specified local axis.

    Usage: IsTouchingSideAxis()(arg1, arg2, axis, dot_product_threshold)
    Args:
        arg1 (BaseObjectState): The object that is touching.
        arg2 (BaseObjectState): The object whose side is being touched.
        axis (str): The local axis of arg2 to check against. Must be 'x', 'y', or 'z'.
        dot_product_threshold (float): A value between 0.0 and 1.0 for alignment tolerance. 
                                     A higher value means stricter alignment. Recommended: ~0.85.
    Returns:
        bool: True if arg1 is touching the specified side of arg2, False otherwise.
    """

    def __call__(self, arg1, arg2, axis, doc_product_threshold):
        axis = axis.lower()
        if axis not in ["x", "y", "z"]:
            raise ValueError("Axis must be one of 'x', 'y', or 'z'")
        
        # 1. Quick check for physical contact
        if not arg1.check_contact(arg2):
            return False
        
        geom1 = arg1.get_geom_state()
        geom2 = arg2.get_geom_state()
        pos1 = geom1["pos"]
        pos2 = geom2["pos"]

        # 2. Calculate the normalized vector from arg1 to arg2
        vector_2_to_1 = np.array(pos2) - np.array(pos1)
        if np.linalg.norm(vector_2_to_1) < 1e-6:
            return False
        vector_2_to_1 /= np.linalg.norm(vector_2_to_1)

        # 4. Determine the direction of arg2's specified local axis
        w, x, y, z = geom2["quat"]
        quat_for_rs = np.array([x, y, z, w])
        R2 = transform_utils.quat2mat(quat_for_rs)

        # 5. Map the specified axis to the corresponding column in the rotation matrix
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        target_axis_vector = R2[:, axis_index]

        # 6. Calculate the dot product to measure alignment
        dot_product = np.dot(vector_2_to_1, target_axis_vector)

        # print(f"Dot product for {axis}-axis: {dot_product:.4f} (Threshold: {doc_product_threshold})")

        return abs(dot_product) >= doc_product_threshold


    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, str, float]


class AxisAlignedWithinObjectAxis(BinaryAtomic):
    """
    Check if the angle between two specified axes of two objects is within a given range.
    
    Usage: AxisAlignedWithinObjectAxis()(obj1, obj2, axis1, axis2, min_deg, max_deg)
    Arguments:
    - obj1: The first object.
    - obj2: The second object.
    - axis1: A string indicating the axis ('x', 'y', or 'z') of the first object.
    - axis2: A string indicating the axis ('x', 'y', or 'z') of the second object.
    - min_deg: Minimum angle in degrees for the axes to be considered aligned.
    - max_deg: Maximum angle in degrees for the axes to be considered aligned.
    
    Returns:
    - True if the angle between the specified axes is within the range [min_deg, max_deg].
    - False otherwise.
    
    Raises:
    - ValueError: If the axes are not one of 'x', 'y', or 'z', or if the degree range is invalid.
    """
    def __call__(self, obj1, obj2, axis1, axis2, min_deg, max_deg):
        if axis1 not in {"x", "y", "z"}:
            raise ValueError("axis1 must be one of 'x', 'y', or 'z'")
        if axis2 not in {"x", "y", "z"}:
            raise ValueError("axis2 must be one of 'x', 'y', or 'z'")
        if not (0 <= min_deg <= max_deg <= 180):
            raise ValueError("Degrees must satisfy 0 <= min_deg <= max_deg <= 180")

        min_rad = np.radians(min_deg)
        max_rad = np.radians(max_deg)
        cos_min = np.cos(min_rad)
        cos_max = np.cos(max_rad)

        # Get the quaternion for the first object
        geom1 = obj1.get_geom_state()
        w1, x1, y1, z1 = geom1["quat"]
        quat1 = np.array([x1, y1, z1, w1])
        R1 = transform_utils.quat2mat(quat1)

        # Get the quaternion for the second object
        geom2 = obj2.get_geom_state()
        w2, x2, y2, z2 = geom2["quat"]
        quat2 = np.array([x2, y2, z2, w2])
        R2 = transform_utils.quat2mat(quat2)

        # Get the specified axis of each object in world coordinates
        axis_index1 = {"x": 0, "y": 1, "z": 2}[axis1]
        axis_index2 = {"x": 0, "y": 1, "z": 2}[axis2]
        object1_axis = R1[:, axis_index1]
        object2_axis = R2[:, axis_index2]

        # Calculate the cosine of the angle between the two axes
        cos_angle = np.dot(object1_axis, object2_axis)
        # Clamp to [-1, 1] to avoid numerical issues
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        # Check if the angle is within the specified range
        # Note: cosine is decreasing as the angle increases from 0 to 180 degrees
        return cos_max <= cos_angle <= cos_min

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, str, str, float, float]
    
class YawAngleAligned(BinaryAtomic):
    """
    Check if the yaw (rotation around z-axis) of two objects are aligned within a specified threshold (in degrees),
    after applying an offset to the second object's yaw.

    Usage: YawAngleAligned()(obj1, obj2, yaw_thresh, yaw_offset)
    Arguments:
    - obj1: The first object.
    - obj2: The second object.
    - yaw_thresh: Allowed deviation for yaw in degrees.
    - yaw_offset: Offset (in degrees) to apply to obj2's yaw before comparison.

    Returns:
    - True if the absolute difference of yaw (with offset) is within its threshold (using acute angle).
    """
    def __call__(self, obj1, obj2, yaw_thresh, yaw_offset):
        geom1 = obj1.get_geom_state()
        geom2 = obj2.get_geom_state()
        w1, x1, y1, z1 = geom1["quat"]
        w2, x2, y2, z2 = geom2["quat"]
        quat1 = np.array([x1, y1, z1, w1])
        quat2 = np.array([x2, y2, z2, w2])
        R1 = transform_utils.quat2mat(quat1)
        R2 = transform_utils.quat2mat(quat2)
        _, _, yaw1 = transform_utils.mat2euler(R1)
        _, _, yaw2 = transform_utils.mat2euler(R2)
        # Convert to degrees
        yaw1 = np.degrees(yaw1)

        def clamp_angle(angle):
            """Clamp any angle to the range [-180, 180] degrees."""
            return ((angle % 360) + 180) % 360 - 180

        yaw2 = clamp_angle(np.degrees(yaw2) + yaw_offset)

        def acute_diff(a, b):
            diff = abs(a - b)
            if diff > 180:
                diff = 360 - diff
            return diff

        within_yaw = acute_diff(yaw1, yaw2) <= yaw_thresh
        return within_yaw

    def expected_arg_types(self):
        return [BaseObjectState, BaseObjectState, float, float]

