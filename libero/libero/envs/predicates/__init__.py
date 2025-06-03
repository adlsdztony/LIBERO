from .base_predicates import *


VALIDATE_PREDICATE_FN_DICT = {
    "true": TruePredicateFn(),
    "false": FalsePredicateFn(),
    "not": Not(),
    "and": And(),
    "or": Or(),
    "any": Any(),
    "all": All(),
    "in": In(),
    "incontact": InContactPredicateFn(),
    "on": On(),
    "relaxedon": RelaxedOn(),
    "up": Up(),
    # "stack":     Stack(),
    "stackbowl": StackBowl(),
    # "temporal":  TemporalPredicate(),
    "printjointstate": PrintJointState(),
    "open": Open(),
    "close": Close(),
    "openratio": OpenRatio(),
    "staircase": StairCase(),
    "inair": InAir(),
    "turnon": TurnOn(),
    "turnoff": TurnOff(),
    "upsidedown": UpsideDown(),
    "upright": Upright(),
    "axisalignedwithin": AxisAlignedWithin(),
    "under": Under(),
    "posigreaterthan": PosiGreaterThan(),
    "positionwithin": PositionWithin(),
    "oncentre":OnCentre(),
    "above": Above(),
    "between": MidBetween(),
}


def update_predicate_fn_dict(fn_key, fn_name):
    VALIDATE_PREDICATE_FN_DICT.update({fn_key: eval(fn_name)()})


def eval_predicate_fn(predicate_fn_name, *args):
    assert predicate_fn_name in VALIDATE_PREDICATE_FN_DICT
    return VALIDATE_PREDICATE_FN_DICT[predicate_fn_name](*args)


def get_predicate_fn_dict():
    return VALIDATE_PREDICATE_FN_DICT


def get_predicate_fn(predicate_fn_name):
    return VALIDATE_PREDICATE_FN_DICT[predicate_fn_name.lower()]