"""
6.101 Lab:
Symbolic Algebra
"""

# import doctest # optional import
# import typing # optional import
# import pprint # optional import
# import string # optional import
# import abc # optional import

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Expr:
    def __add__(self, other):
        return Add(self, other)
    
    def __radd__(self, other):
        return Add(other, self) 
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __rsub__(self, other):
        return Sub(other, self)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __rmul__(self, other):
        return Mul(other, self)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __rtruediv__(self, other):
        return Div(other, self)

class BinOp(Expr):
    """
    Parent class for binary operations (operations with left and right operands).
    """
    #Since all the subclasses use the same init function, we can 
    #just define it in the parent class
    def __init__(self, left, right):
        """
        Initializer.  Store instance variables called `left` and `right`,
        containing the values passed in to the initializer.
        """
        if type(left) in [int, float]:
            self.left = Num(left)
        elif type(left) == str:
            self.left = Var(left)
        else:
            self.left = left

        if type(right) in [int, float]:
            self.right = Num(right)
        elif type(right) == str:
            self.right = Var(right)
        else:
            self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    precedence = 0

class Add(BinOp):
    precedence = 1

    def __str__(self):
        return f"{self.left} + {self.right}"

    def evaluate(self, mapping):
        return self.left.evaluate(mapping) + self.right.evaluate(mapping)

class Sub(BinOp):
    precedence = 1

    def __str__(self):
        if self.right.precedence == self.precedence:
            right_str = "(" + str(self.right) + ")"
        else:
            right_str = str(self.right)
        return f"{self.left} - {right_str}"

    def evaluate(self, mapping):
        return self.left.evaluate(mapping) - self.right.evaluate(mapping)
    
class Mul(BinOp):
    precedence = 2
    def __str__(self):
        if self.left.precedence < self.precedence:
            left_str = "(" + str(self.left) + ")"
        else:
            left_str = str(self.left)
        if self.right.precedence < self.precedence:
            right_str = "(" + str(self.right) + ")"
        else:
            right_str = str(self.right)
        return f"{left_str} * {right_str}"
    
    def evaluate(self, mapping):
        return self.left.evaluate(mapping) * self.right.evaluate(mapping)

class Div(BinOp):
    precedence = 2
    def __str__(self):
        if self.left.precedence < self.precedence:
            left_str = "(" + str(self.left) + ")"
        else:
            left_str = str(self.left)
        if self.right.precedence <= self.precedence:
            right_str = "(" + str(self.right) + ")"
        else:
            right_str = str(self.right)
        return f"{left_str} / {right_str}"

    def evaluate(self, mapping):
        return self.left.evaluate(mapping) / self.right.evaluate(mapping)

class Var(Expr):
    def __init__(self, name):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"
    
    precedence = 3

    def evaluate(self, mapping):
        if self.name in mapping:
            return mapping[self.name]
        else:
            raise SymbolicEvaluationError(f"Variable '{self.name}' not found in mapping.")      


class Num(Expr):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
    
    precedence = 3

    def evaluate(self, mapping):
        return self.n

class SymbolicEvaluationError(Exception):
    """
    An expression indicating that something has gone wrong when evaluating a
    symbolic algebra expression.
    """
    pass


if __name__ == "__main__":
    pass
