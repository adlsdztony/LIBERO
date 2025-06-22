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
    

class Constraint(PredicateWrapper):
    def __init__(self):
        super().__init__()
        self.constraint_satisfied = {}
        
    def __call__(self, name, arg):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def expected_arg_types(self):
        return [bool]


class ConstraintAlways(Constraint):
    def __call__(self, name, arg):
        if name not in self.constraint_satisfied:
            self.constraint_satisfied[name] = True
        self.constraint_satisfied[name] = arg and self.constraint_satisfied[name]
        return self.constraint_satisfied[name]


class ConstraintNever(Constraint):
    def __call__(self, name, arg):
        if name not in self.constraint_satisfied:
            self.constraint_satisfied[name] = True
        self.constraint_satisfied[name] = not arg and self.constraint_satisfied[name]
        return self.constraint_satisfied[name]


class ConstraintOnce(Constraint):
    def __call__(self, name, arg):
        if name not in self.constraint_satisfied:
            self.constraint_satisfied[name] = False
        self.constraint_satisfied[name] = arg or self.constraint_satisfied[name]
        return self.constraint_satisfied[name]