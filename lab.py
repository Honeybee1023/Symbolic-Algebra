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
    pass

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

class Add(BinOp):
    def __str__(self):
        return f"({self.left} + {self.right})"

class Sub(BinOp):
    def __str__(self):
        return f"({self.left} - {self.right})"
    
class Mul(BinOp):
    def __str__(self):
        return f"({self.left} * {self.right})"

class Div(BinOp):
    def __str__(self):
        return f"({self.left} / {self.right})"

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


if __name__ == "__main__":
    pass
