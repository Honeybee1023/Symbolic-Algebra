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

    # Since all the subclasses use the same init function, we can
    # just define it in the parent class
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

    def deriv(self, var):
        return self.left.deriv(var) + self.right.deriv(var)

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left == Num(0):
            return right
        if right == Num(0):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n + right.n)
        return left + right


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

    def deriv(self, var):
        return self.left.deriv(var) - self.right.deriv(var)

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if right == Num(0):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n - right.n)
        return left - right


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

    def deriv(self, var):
        return (self.left.deriv(var) * self.right) + (self.left * self.right.deriv(var))

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left == Num(0) or right == Num(0):
            return Num(0)
        if left == Num(1):
            return right
        if right == Num(1):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n * right.n)
        return left * right


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

    def deriv(self, var):
        numerator = (self.left.deriv(var) * self.right) - (
            self.left * self.right.deriv(var)
        )
        denominator = self.right * self.right
        return numerator / denominator

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if left == Num(0):
            return Num(0)
        if right == Num(1):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(left.n / right.n)
        return left / right


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

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.name == other.name
        return False

    precedence = 3

    def evaluate(self, mapping):
        if self.name in mapping:
            return mapping[self.name]
        else:
            raise SymbolicEvaluationError(
                f"Variable '{self.name}' not found in mapping."
            )

    def deriv(self, var):
        if self.name == var:
            return Num(1)
        else:
            return Num(0)

    def simplify(self):
        return self


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

    def __eq__(self, other):
        if isinstance(other, Num):
            return self.n == other.n
        return False

    precedence = 4

    def evaluate(self, mapping):
        return self.n

    def deriv(self, var):
        return Num(0)

    def simplify(self):
        return self


class SymbolicEvaluationError(Exception):
    """
    An expression indicating that something has gone wrong when evaluating a
    symbolic algebra expression.
    """

    pass


def tokenize(string):
    """
    Each string character is a token. Each full number is a token.
    """
    tokens = []
    current_number = ""
    has_dot = False
    prev_ch = None
    for ch in string:
        # allow leading '-' as part of number when at start or after '(' or operator
        if (
            ch == "-"
            and current_number == ""
            and (prev_ch is None or prev_ch in "(+ -*/")
        ):
            current_number += ch
        elif ch.isdigit():
            current_number += ch
        elif ch == "." and not has_dot and current_number != "":
            # only allow max one decimal point inside a number
            current_number += ch
            has_dot = True
        else:
            if current_number != "":
                tokens.append(current_number)
                current_number = ""
                has_dot = False
            if ch.strip() != "":
                tokens.append(ch)
        prev_ch = ch
    if current_number != "":
        tokens.append(current_number)
    return tokens


def parse(tokens):
    """
    Parse a list of tokens and return the parsed expression.

    >>> repr(parse(tokenize("3")))
    'Num(3)'
    >>> repr(parse(tokenize("x")))
    "Var('x')"
    >>> repr(parse(tokenize("(1+2)")))
    'Add(Num(1), Num(2))'
    >>> repr(parse(tokenize("(x*(y+1))")))
    "Mul(Var('x'), Add(Var('y'), Num(1)))"
    """

    def parse_expression(index):
        token = tokens[index]

        # try to parse as integer first, then float
        try:
            # first try int conversion
            if token.isdigit():
                return Num(int(token)), index + 1
            # then try float conversion
            num = float(token)
            return Num(num), index + 1
        except Exception:
            pass

        # parse single alphabetic character as variable
        if len(token) == 1 and token.isalpha():
            return Var(token), index + 1

        # Otherwise ( E1 op E2 )
        if token != "(":
            raise ValueError(f"Unexpected token at {index}: {token}")

        # parse left expression starting after '('
        left_expr, next_index = parse_expression(index + 1)

        op_token = tokens[next_index]
        if op_token not in ["+", "-", "*", "/"]:
            raise ValueError(f"Expected operator at {next_index}, got {op_token}")

        # parse right expression after operator
        right_expr, next_index2 = parse_expression(next_index + 1)

        # next token must be ')'
        if tokens[next_index2] != ")":
            raise ValueError(
                f"Expected ')' at {next_index2}, got {tokens[next_index2]}"
            )

        # make BinOp
        if op_token == "+":
            node = Add(left_expr, right_expr)
        elif op_token == "-":
            node = Sub(left_expr, right_expr)
        elif op_token == "*":
            node = Mul(left_expr, right_expr)
        else:
            node = Div(left_expr, right_expr)

        return node, next_index2 + 1

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression


def make_expression(string):
    tokens = tokenize(string)
    return parse(tokens)


if __name__ == "__main__":
    # Tests:
    print(tokenize(" (x + -3.0) * y / 21 "))
    print(repr(parse(tokenize("3"))))
    print(repr(parse(tokenize("x"))))
    print(repr(parse(tokenize("(1+2)"))))
    print(repr(parse(tokenize("(x*(y+1))"))))
    print(repr(make_expression("(x * (2 + 3))")))
