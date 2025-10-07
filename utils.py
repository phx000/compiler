import operator
from collections import namedtuple, defaultdict
from enum import Enum
from functools import cache


class Type(Enum):
    VAR = "var"
    OP = "op"

# todo test this file
class Op(Enum):
    ADD = ("+", 2, operator.add)
    SUB = ("-", 2, operator.sub)
    MUL = ("*", 3, operator.mul)
    # DIV = ("/", 3, operator.truediv)  # todo handle floats

    EQ = ("==", 1, operator.eq)
    NEQ = ("!=", 1, operator.ne)
    LT = ("<", 1, operator.lt)
    LTE= ("<=", 1, operator.le)
    GTE = (">=", 1, operator.ge)
    GT = (">", 1, operator.gt)

    # logical
    AND = ("&", 0, operator.and_)
    OR = ("|", 0, operator.or_)
    NOT = ("!", 4, operator.not_)

    # todo implement POW and TRUTH

    def __init__(self, symbol, prio, fn):
        self.symbol = symbol
        self.prio = prio
        self.fn = fn

    @classmethod
    @cache
    def operators_by_priority(cls):
        d = defaultdict(list)

        for op in cls:
            d[op.prio].append(op)

        return dict(d)


Part = namedtuple("Part", ["type", "value"])
