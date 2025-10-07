from errors import InvalidOperatorPlacementError
from utils import Op

type NestedPartList = list[int | Op | "NestedPartList"]


def calc(parts: NestedPartList) -> int | None:
    if not parts:
        return None

    result = 0

    while parts:
        part = parts.pop(0)

        # case when expression starts with sub-expression
        if isinstance(part, list):
            result = calc(part)
            continue

        # case when expression starts with a number
        if isinstance(part, int):
            result = part
            continue

        # case when expression starts with an operator
        if not parts:
            raise InvalidOperatorPlacementError("Expression cannot end in an operator")

        next_part = parts.pop(0)
        right = calc([next_part])

        if right is None:
            raise InvalidOperatorPlacementError("Expression cannot end in an operator")

        result = part.fn(result, right)

    return result

# tparts = [
#     Op.SUB,
#     [
#         8,
#         Op.ADD,
#         4
#     ],
#     Op.SUB,
#     [
#         2,
#         Op.ADD,
#         [
#             1,
#             Op.SUB,
#             4
#         ],
#     ],
# ]
# print(calc(tparts))

# def calc_parts_p(parts):
#     result = None
#
#     if not parts:
#         return None
#
#     while parts:
#         part = parts.pop(0)
#
#         if isinstance(part, list):
#             return calc_parts(part)
#
#         t, val = part
#
#         if t is Type.VAR:
#             if not parts:
#                 return val
#
#             part2 = parts.pop(0)
#
#             if isinstance(part2, list):
#                 raise ValueError("A number must be separated from the next construct with an operator")
#
#             t2, op = part2
#
#             if t2 is Type.VAR:
#                 raise ValueError("A number must be separated from the next construct with an operator")
#
#             right = calc_parts(parts)
#
#             if right is None:
#                 raise ValueError("Expression cannot end in an operator")
#
#             if result is None:
#                 result = val
#
#             result = op.run(result, right)
#
#         if t is Type.OP:
#             if val not in (Op.ADD, Op.SUB):
#                 raise ValueError(f"Expression cannot start with operator '{t.value}'")
#
#             if not parts:
#                 raise ValueError("Expression cannot end in an operator")
#
#             part2 = parts.pop(0)
#
#             if isinstance(part2, tuple) and part2[0] is Type.OP:
#                 raise ValueError("Two consecutive operators are not allowed")
#
#             result = val.run(0, part2[1])


# if val in (Op.ADD, Op.SUB):
#     left = 0 if result is None else result
# elif result is None:
#     raise ValueError(f"Expression cannot start with operator '{t.value}'")
# else:
#     left = result
#
# right = calc_parts(parts)
#
# if right is None:
#     raise ValueError("Expression cannot end in an operator")
#
# result = val.run(left, right)

# return result

# else:
#     if result is None:
#         raise ValueError(f"Expression cannot start with operator '{t.value}'")
#
#     right = calc_parts(parts)
#
#     if right is None:
#         raise ValueError(f"Expression cannot end in an operator")
#
#     result = val.run(result, right)


# PARSER

# def calc(s, parts=None):
#     cur = 0
#
#     if parts is None:
#         parts = []
#
#     while cur < len(s):
#         if s[cur] == " ":
#             cur += 1
#             continue
#
#         num = ""
#
#         while s[cur].isnumeric():
#             num += s[cur]
#             cur += 1
#
#         if num:
#             parts += (Type.VAR, int(num))
#             continue
#
#         elif s[cur] in [o.value for o in Op]:
#             parts += (Type.OP, Op(s[cur]))
#             cur += 1
#             continue
#
#         elif s[cur] == "(":
#             parts += calc(s[cur + 1:], parts)
#
#         elif s[cur] == ")":
#             return parts
#
#         else:
#             raise ValueError(f"Invalid character: {s[cur]}")

# for part in parts:


# parts=[(Type.VAR, 4), (Type.OP, Op.ADD), [(Type.VAR,2), (Type.OP, Op.SUB), (Type.VAR,8)]]
