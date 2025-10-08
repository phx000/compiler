from utils import Op

type ExpressionParts = list[int | Op | "ExpressionParts"]


# todo add validation that errors when higher prio binary operator is applied to lower prio unary operator chain
#   coming immediately after. e.g: "3 + !5" will error because "+" is higher prio than "!". The current code will
#   pass "!" (Op.NOT) into Op.ADD.fn().

def calc(parts: ExpressionParts) -> int:
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
            result = op.fn(left, right)
            parts = parts[:op_idx - 1] + [result] + parts[op_idx + 2:]

    return parts[0]

# print(
#     calc(
#         [
#             3,
#             Op.ADD,
#             5,
#             Op.MUL,
#             [
#                 5,
#                 Op.ADD,
#                 [
#                     Op.NOT,
#                     Op.NEG,
#                     Op.NOT,
#                     7,
#                 ],
#             ],
#             Op.ADD,
#             5,
#             Op.POW,
#             2
#         ]
#     )
# )
# print(
#     3 + 5 * (5 + (not -(not 7))) + 5 ** 2
# )
