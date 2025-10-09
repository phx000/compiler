import operator
import string
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import NamedTuple


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

    def __repr__(self):
        return f"Op({self.name})"

    @classmethod
    def from_symbol(cls, symbol):
        # to reference members with a duplicate symbol (like SUB and NEG), use from_operator_fn
        return cls.unique_symbol_to_member_map()[symbol]

    @classmethod
    @cache
    def from_name(cls, name):
        return getattr(cls, name)

    @classmethod
    @cache
    def unique_symbol_to_member_map(cls):
        # duplicate symbols and their corresponding members are removed from the result
        symbols = [op.symbol for op in cls]
        counter = Counter(symbols)
        return {op.symbol: op for op in cls if counter[op.symbol] == 1}

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


VAR_NAME_START_CHARS = string.ascii_letters + "_"
VAR_NAME_CHARS = VAR_NAME_START_CHARS + string.digits


@dataclass
class Instr:
    # Base class. Should not be instantiated
    pass


@dataclass
class DeclareIntInstr(Instr):
    name: str
    expr: str


@dataclass
class SetVarInstr(Instr):
    name: str
    expr: str


@dataclass
class PrintInstr(Instr):
    expr: str


@dataclass
class CondInstr(Instr):
    cond: str
    instrs: list[Instr]
    instrs_else: list[Instr]


@dataclass
class LoopInstr(NamedTuple):
    cond: str
    instrs: list[Instr]
