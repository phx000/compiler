import operator
from collections import namedtuple, defaultdict
from enum import Enum
from functools import cache


class Type(Enum):
    VAR = "var"
    OP = "op"


# todo test this file
class Op(Enum):
    # boolean
    OR = ("|", 0, operator.or_)
    AND = ("&", 1, operator.and_)
    NOT = ("!", 2, operator.not_)

    EQ = ("==", 3, operator.eq)
    NEQ = ("!=", 3, operator.ne)
    LT = ("<", 3, operator.lt)
    LTE = ("<=", 3, operator.le)
    GTE = (">=", 3, operator.ge)
    GT = (">", 3, operator.gt)

    ADD = ("+", 4, operator.add)
    SUB = ("-", 4, operator.sub)
    MUL = ("*", 5, operator.mul)
    # DIV = ("/", 5, operator.truediv)  # todo handle floats
    POW = ("^", 6, operator.pow)
    NEG = ("-", 7, operator.neg)

    def __init__(self, symbol, prio, fn):
        self.symbol = symbol
        self.prio = prio
        self.fn = fn

    @classmethod
    def unary(cls):
        return cls.NOT, cls.NEG

    @classmethod
    @cache
    def operators_by_priority(cls):
        d = defaultdict(list)

        for op in cls:
            d[op.prio].append(op)

        return dict(d)

    @property
    def is_unary(self):
        return self in self.__class__.unary()


Part = namedtuple("Part", ["type", "value"])
