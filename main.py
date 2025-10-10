from typing import cast

from parsers import parse_expression
from utils import Op, Instr, SetVarInstr, LoopInstr, CondInstr, DeclareIntInstr, PrintInstr, Expression, VarStack, \
    UnresolvedExpression


# todo add a typechecker + pre-commit to the project

def calc_expression(parts: Expression) -> int:
    for i, part in enumerate(parts):
        if isinstance(part, list):
            parts[i] = calc_expression(part)

    for i in range(len(parts) - 1):
        p1, p2 = parts[i], parts[i + 1]

        if isinstance(p1, int) and isinstance(p2, int):
            raise ValueError("Expressions cannot contain consecutive numbers")

    while len(parts) > 1:
        max_prio = 0
        op_idx = None  # index of the first operator with the highest priority in the expression

        for i, part in enumerate(parts):
            if isinstance(part, Op) and part.prio > max_prio:
                max_prio = part.prio
                op_idx = i

        op = parts[op_idx]

        if op.is_unary:
            op_chain = [op]  # list of unary operators preceding a number
            val = None
            offset = 1

            while op_idx + offset < len(parts):
                part = parts[op_idx + offset]

                if isinstance(part, int):
                    val = part
                    break

                if not part.is_unary:
                    raise ValueError("A binary operator cannot be declared after a unary operator")

                op_chain.append(part)
                offset += 1

            if val is None:
                raise ValueError("Expressions cannot end in an operator")

            for unary_op in reversed(op_chain):
                val = unary_op.fn(val)

            parts = parts[:op_idx] + [val] + parts[op_idx + len(op_chain) + 1:]

        else:
            if op_idx == 0:
                raise ValueError(f"Expression cannot start with operator '{op.symbol}'")

            if op_idx == len(parts) - 1:
                raise ValueError("Expression cannot end in an operator")

            left = parts[op_idx - 1]
            right = parts[op_idx + 1]

            if isinstance(right, Op):
                raise ValueError(f"Operator '{op.symbol}' cannot be used with '{right.symbol}'")

            result = op.fn(left, right)
            parts = parts[:op_idx - 1] + [result] + parts[op_idx + 2:]

    return parts[0]


def get_var(name: str, var_stack: VarStack) -> int:
    for dct in reversed(var_stack):
        if (val := dct.get(name)) is not None:
            return val

    raise KeyError(f"Variable '{name}' not defined")


def set_var(name: str, val: int, var_stack: VarStack) -> None:
    for dct in reversed(var_stack):
        if name in dct:
            dct[name] = val
            return

    raise KeyError(f"Variable '{name}' not defined")


def resolve_expression_vars(parts: UnresolvedExpression, var_stack: VarStack) -> Expression:
    for i, part in enumerate(parts):
        if isinstance(part, list):
            parts[i] = resolve_expression_vars(part, var_stack)

        elif isinstance(part, str):
            parts[i] = get_var(part, var_stack)

    return cast(Expression, parts)


def resolve_expression(expr: str, var_stack: VarStack) -> int:
    unres_expr = parse_expression(expr)
    expr = resolve_expression_vars(unres_expr, var_stack)
    return calc_expression(expr)


def resolve_instructions(instructions: list[Instr], var_stack: VarStack | None = None) -> None:
    var_stack = var_stack or []
    var_stack.append({})

    for instr in instructions:
        if isinstance(instr, DeclareIntInstr):
            if instr.name in var_stack[-1]:
                raise ValueError(f"Variable '{instr.name}' is already defined locally")

            res = resolve_expression(instr.expr, var_stack)
            var_stack[-1][instr.name] = res

        elif isinstance(instr, SetVarInstr):
            res = resolve_expression(instr.expr, var_stack)
            set_var(instr.name, res, var_stack)

        elif isinstance(instr, PrintInstr):
            res = resolve_expression(instr.expr, var_stack)
            print(res)

        elif isinstance(instr, CondInstr):
            res = resolve_expression(instr.cond, var_stack)
            cont_instr = instr.instrs if res else instr.instrs_else
            resolve_instructions(cont_instr, var_stack)

        # todo implement break and continue in loops
        elif isinstance(instr, LoopInstr):
            while resolve_expression(instr.cond, var_stack):
                resolve_instructions(instr.instrs, var_stack)

        # todo add an exit instr

    var_stack.pop()

# # Test
# resolve_instructions([
#     DeclareIntInstr("a", "5"),
#     PrintInstr("a")
# ])
