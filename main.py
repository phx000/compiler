from utils import Op

type Expression = list[int | Op | "Expression"]


def calc(parts: Expression) -> int:
    for i, part in enumerate(parts):
        if isinstance(part, list):
            parts[i] = calc(part)

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


# s=" 1 + (2 - (5 + 4)) + 1"

"""
1
1, +
1, +, []
1, +, [2]
1, +, [2, -]
1, +, [2, -, []]
"""


def get_active_expression(parts: Expression, depth: int) -> Expression:
    expr = parts

    for d in range(depth):
        expr = expr[-1]

    return expr


def parse_expression(s: str) -> Expression:
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

        elif s[i].isnumeric():
            num = s[i]
            i += 1

            while i < len(s) and s[i].isnumeric():
                num += s[i]
                i += 1

            expr = get_active_expression(parts, depth)
            expr.append(int(num))

        elif s[i]==" ":
            i+=1

        else:
            raise ValueError(f"Invalid character '{s[i]}'")

    return parts


# e = "1+2--(12-!(1-2))"
# print(parse_expression(e))