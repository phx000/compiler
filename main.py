from typing import cast

from utils import Op, Instr, VAR_NAME_CHARS, VAR_NAME_START_CHARS, SetVarInstr, LoopInstr, \
    CondInstr, DeclareIntInstr, PrintInstr

type Expression = list[int | Op | "Expression"]
type UnresolvedExpression = list[int | Op | str | "UnresolvedExpression"]
type VarStack = list[dict[str, int]]


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


def get_active_expression(parts: UnresolvedExpression, depth: int) -> UnresolvedExpression:
    expr = parts

    for d in range(depth):
        expr = expr[-1]

    return expr


def parse_expression(s: str) -> UnresolvedExpression:
    parts = []
    depth = 0
    i = 0

    while i < len(s):
        if s[i] == "(":
            expr = get_active_expression(parts, depth)
            expr.append([])
            depth += 1
            i += 1

        elif s[i] == ")":
            if depth == 0:
                raise ValueError("Extra closing parenthesis")

            depth -= 1
            i += 1

        elif s[i] == "-":
            expr = get_active_expression(parts, depth)

            if expr and isinstance(expr[-1], int):
                expr.append(Op.SUB)
            else:
                expr.append(Op.NEG)

            i += 1

        elif (op := Op.unique_symbol_to_member_map().get(s[i])) is not None:
            expr = get_active_expression(parts, depth)
            expr.append(op)
            i += 1

        # todo make variable parser respect reserved keywords
        elif s[i] in VAR_NAME_START_CHARS:
            name = s[i]
            i += 1

            while i < len(s) and s[i] in VAR_NAME_CHARS:
                name += s[i]
                i += 1

            expr = get_active_expression(parts, depth)
            expr.append(name)

        elif s[i].isnumeric():
            num = s[i]
            i += 1

            while i < len(s) and s[i].isnumeric():
                num += s[i]
                i += 1

            if i < len(s) and s[i] in VAR_NAME_START_CHARS:
                raise ValueError("Variable names cannot start with a number")

            expr = get_active_expression(parts, depth)
            expr.append(int(num))

        elif s[i] == " ":
            i += 1

        else:
            raise ValueError(f"Invalid character '{s[i]}'")

    return parts


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

        elif isinstance(instr, LoopInstr):
            while resolve_expression(instr.cond, var_stack):
                resolve_instructions(instr.instrs, var_stack)

    var_stack.pop()
