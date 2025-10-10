# import pytest
#
# from errors import InvalidOperatorPlacementError, InvalidExpressionError
# from main import calc_expression
# from utils import Type, Op, Part
#
#
# # Tests for expressions with 1 part
# def test_calc_works_with_single_number():
#     parts = [Part(Type.VAR, 3)]
#     assert calc_expression(parts) == 3
#
#
# def test_calc_fails_with_single_operator():
#     parts = [Part(Type.OP, Op.ADD)]
#
#     with pytest.raises(InvalidOperatorPlacementError):
#         calc_expression(parts)
#
#
# # Tests for expressions with leading operators
# def test_calc_works_with_leading_add_and_sub():
#     parts = [Part(Type.OP, Op.ADD), Part(Type.VAR, 3)]
#     assert calc_expression(parts) == 3
#
#     parts = [Part(Type.OP, Op.SUB), Part(Type.VAR, 3)]
#     assert calc_expression(parts) == -3
#
#
# def test_calc_fails_with_invalid_leading_operator():
#     parts = [Part(Type.OP, Op.MUL), Part(Type.VAR, 3)]
#
#     with pytest.raises(InvalidOperatorPlacementError):
#         calc_expression(parts)
#
#
# # Tests for expressions with multiple parts
# def test_calc_works_with_expressions_with_multiple_parts():
#     parts = [
#         Part(Type.VAR, 1),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 2),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 3),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 4)
#     ]
#     assert calc_expression(parts) == 1 + 2 + 3 + 4
#
#
# def test_calc_fails_with_expression_ending_in_operator():
#     parts = [Part(Type.VAR, 3), Part(Type.OP, Op.ADD)]
#
#     with pytest.raises(InvalidOperatorPlacementError):
#         calc_expression(parts)
#
#
# def test_calc_fails_with_two_consecutive_numbers():
#     # Case where expression starts with 2 consecutive numbers
#     parts = [
#         Part(Type.VAR, 2),
#         Part(Type.VAR, 2),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 1),
#     ]
#
#     with pytest.raises(InvalidExpressionError):
#         calc_expression(parts)
#
#     # Case where 2 consecutive numbers are in the middle of an expression
#     parts = [
#         Part(Type.VAR, 1),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 2),
#         Part(Type.VAR, 3),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 4),
#     ]
#
#     with pytest.raises(InvalidExpressionError):
#         calc_expression(parts)
#
#
# def test_calc_fails_with_two_consecutive_operators():
#     # Case where expression starts with 2 consecutive operators
#     parts = [
#         Part(Type.VAR, Op.ADD),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 2),
#     ]
#
#     with pytest.raises(InvalidOperatorPlacementError):
#         calc_expression(parts)
#
#     # Case where 2 consecutive operators are in the middle of an expression
#     parts = [
#         Part(Type.VAR, 1),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 2),
#         Part(Type.OP, Op.ADD),
#         Part(Type.OP, Op.ADD),
#         Part(Type.VAR, 3),
#     ]
#
#     with pytest.raises(InvalidOperatorPlacementError):
#         calc_expression(parts)
#
#
# def test_calc_fails_with_two_consecutive_expressions():
#     # Case where expression starts with 2 consecutive sub-expressions
#     two_subs = [
#                    Part(Type.VAR, 3),
#                    Part(Type.OP, Op.ADD),
#                    Part(Type.VAR, 3)
#                ] * 2
#
#     with pytest.raises(InvalidExpressionError):
#         calc_expression(two_subs)
#
#     # Case where 2 consecutive sub-expressions are in the middle of an expression
#     parts = [
#         Part(Type.VAR, 1),
#         Part(Type.OP, Op.ADD),
#         two_subs
#     ]
#
#     with pytest.raises(InvalidOperatorPlacementError):
#         calc_expression(parts)
#
#
# # Nested expressions tests
# def test_calc_works_with_nested_expressions():
#     parts = [
#         [
#             Part(Type.VAR, 26),
#             Part(Type.OP, Op.SUB),
#             Part(Type.VAR, 14),
#         ],
#         Part(Type.OP, Op.SUB),
#         [
#             Part(Type.VAR, 8),
#             Part(Type.OP, Op.SUB),
#             [
#                 Part(Type.VAR, 11),
#                 Part(Type.OP, Op.SUB),
#                 Part(Type.VAR, 7),
#             ]
#         ]
#     ]
#     assert calc_expression(parts) == (26 - 14) - (8 - (11 - 7))
#
#
# # Operator hierarchy tests
# def test_calc_respects_operator_hierarchy():
#     ops=Op.operators_by_priority()
#
