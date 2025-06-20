from .base_predicates import Expression
from typing import List

class PredicateWrapper(Expression):
    """
    A wrapper for predicates that allows them to be used as expressions.
    This class is used to wrap predicates so they can be used in the expression
    system of the environment.
    """

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("PredicateWrapper should not be called directly. Use a specific predicate class instead.")

    def expected_arg_types(self) -> List[type]:
        raise NotImplementedError
    
    def __str__(self):
        return f"{self.__class__.__name__}()"


class BoolResultWrapper:
    def __init__(self, result: bool, print_result):
        self.result = result
        self.print_result = print_result
    
    def __bool__(self):
        return self.result

    def __str__(self):
        return f"{self.print_result}"
    

class Watch(PredicateWrapper):
    def __call__(self, args):
        return BoolResultWrapper(True, args)

    def expected_arg_types(self) -> List[type]:
        return [bool]


class StatefulWrapper(PredicateWrapper):
    def __init__(self):
        super().__init__()
        self.state = {}

    def __call__(self, name, *arg):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def reset(self):
        self.state.clear()
    
    def expected_arg_types(self):
        raise NotImplementedError("Subclasses should implement this method.")
    

class Constraint(StatefulWrapper):
    def expected_arg_types(self):
        return [bool]


class ConstraintAlways(Constraint):
    def __call__(self, name, *arg):
        if len(arg) != 1:
            raise ValueError("ConstraintAlways expects exactly one argument.")
        if name not in self.state:
            self.state[name] = True
        self.state[name] = arg[0] and self.state[name]
        return self.state[name]


class ConstraintNever(Constraint):
    def __call__(self, name, *arg):
        if len(arg) != 1:
            raise ValueError("ConstraintNever expects exactly one argument.")
        if name not in self.state:
            self.state[name] = True
        self.state[name] = not arg[0] and self.state[name]
        return self.state[name]


class ConstraintAlwaysAfter(Constraint):
    def __call__(self, name, *arg):
        if len(arg) != 2:
            raise ValueError("ConstraintAlwaysAfter expects exactly two arguments.")
        if name not in self.state:
            self.state[name] = (False, True)
        if not self.state[name][0]:
            self.state[name] = (arg[0], self.state[name][1])
        else:
            self.state[name] = (self.state[name][0], arg[1] and self.state[name][1])
        return self.state[name][0] and self.state[name][1]
    
    def expected_arg_types(self):
        return [bool, bool]  # Expecting a tuple of (name, arg)

class ConstraintOnce(Constraint):
    def __call__(self, name, *arg):
        if name not in self.state:
            self.state[name] = False
        self.state[name] = arg[0] or self.state[name]
        return self.state[name]


class Sequential(StatefulWrapper):
    """
    A wrapper for predicates that enforces a sequential order of execution.
    This class is used to ensure that predicates are satisfied in a specific order.
    """
    def __call__(self, name, *arg):
        """
        Check if the current state is a continuation of the last state.

        Args:
            name (str): The name of the predicate.
            arg (tuple): tuple of bool objects representing the current state.
        """
        arg = arg[0]

        if name not in self.state:
            self.state[name] = {
                "Sequential": True,
                "LastState": [False] * len(arg),
                "NextExpectedIndex": 0
                }

        if not self.state[name]["Sequential"]:
            return BoolResultWrapper(False, f"{arg} Failed")
        
        # Sequential means: once a position becomes True, it stays True
        # and new True values can only appear at the next expected position
        for i in range(len(arg)):
            # If a previously True value becomes False, it's not sequential
            if self.state[name]["LastState"][i] and not arg[i]:
                self.state[name]["Sequential"] = False
                return BoolResultWrapper(False, f"{arg} Failed")
            
            # If a new True appears, it must be at the next expected sequential position
            if not self.state[name]["LastState"][i] and arg[i]:
                if i != self.state[name]["NextExpectedIndex"]:
                    self.state[name]["Sequential"] = False
                    return BoolResultWrapper(False, f"{arg} Failed")
                self.state[name]["NextExpectedIndex"] += 1
        
        # Update the last state
        self.state[name]["LastState"] = list(arg)
        return BoolResultWrapper(all(arg), f"{arg} Is Sequential")

    def expected_arg_types(self):
        return [tuple]


class RelaxedSequential(StatefulWrapper):
    """
    A wrapper for predicates that enforces sequential progression without persistence.
    Similar to Sequential, but allows previously achieved positions to become False again.
    Only requires that new True values appear in sequential order (starting from arg[0]).
    """
    def __call__(self, name, *arg):
        """
        Check if new True values appear in sequential order.

        Args:
            name (str): The name of the predicate.
            arg (tuple): tuple of bool objects representing the current state.
        """
        arg = arg[0]

        if name not in self.state:
            self.state[name] = {
                "Sequential": True,
                "LastState": list(arg),
                "NextExpectedIndex": 0
                }

        if not self.state[name]["Sequential"]:
            return BoolResultWrapper(False, f"{arg} Failed")
        
        # RelaxedSequential means: once a position becomes True, it can become False again,
        # and new True values can only appear at the next expected position
        for i in range(self.state[name]["NextExpectedIndex"], len(arg)):
            # If a new True appears, it must be at the next expected sequential position
            if not self.state[name]["LastState"][i] and arg[i]:
                if i != self.state[name]["NextExpectedIndex"]:
                    self.state[name]["Sequential"] = False
                    return BoolResultWrapper(False, f"{arg} Failed")
                self.state[name]["NextExpectedIndex"] += 1
        
        # Update the last state
        self.state[name]["LastState"] = list(arg)

        return BoolResultWrapper(arg[-1], f"{arg} Is Relaxed Sequential")

    def expected_arg_types(self):
        return [tuple]