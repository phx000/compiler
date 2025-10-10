import string

from utils import Op, VAR_NAME_START_CHARS, VAR_NAME_CHARS, Instr, UnresolvedExpression, Kws, SetVarInstr, \
    DeclareIntInstr, PrintInstr, CondInstr, LoopInstr


# todo make all parses ignore string.whitespace instead of " "
# todo improve error messages

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

        elif s[i] in string.whitespace:
            i += 1

        else:
            raise ValueError(f"Invalid character '{s[i]}'")

    return parts


def get_active_expression(parts: UnresolvedExpression, depth: int) -> UnresolvedExpression:
    expr = parts

    for d in range(depth):
        expr = expr[-1]

    return expr


def parse_word(s, i, allow_empty=False):
    if i >= len(s):
        raise ValueError("Incomplete instruction")

    word = ""

    while i < len(s):
        if s[i] in VAR_NAME_START_CHARS:
            word += s[i]
            i += 1

            while i < len(s) and s[i] in VAR_NAME_CHARS:
                word += s[i]
                i += 1

            return word, i

        elif s[i] in string.whitespace:
            i += 1

        else:
            raise ValueError(f"Expecting word but got '{s[i]}'")

    if not allow_empty and not word:
        raise ValueError("Expecting word")

    return word, i


def find_substr(sub, s, i, immediate=True):
    # If immediate is True, it will ensure there is no non-whitespace character before the found occurrence

    if i >= len(s):
        raise ValueError("Incomplete instruction")

    idx = s.find(sub, i)

    if idx == -1:
        raise ValueError("Incomplete instruction")

    if immediate:
        for j in range(i, idx):
            if s[j] not in string.whitespace:
                raise ValueError("Invalid character")

    return idx + len(sub)


def extract_from_bounds(start: str, end: str, s, i):
    start_idx = find_substr(start, s, i)
    end_idx = find_substr(end, s, start_idx, immediate=False) - 1
    return s[start_idx:end_idx], end_idx + 1


# def parse_assignment(s, i):
#     name, i = parse_word(s, i)
#     expr, i = extract_from_bounds("=", ";", s, i)
#     return name, expr, i


def parse_instruction(s: str, i: int) -> tuple[Instr | None, int]:
    word, i = parse_word(s, i, allow_empty=True)

    if not word:  # when instruction is whitespace
        return None, i

    if word not in Kws.values():
        expr, i = extract_from_bounds("=", ";", s, i)
        return SetVarInstr(word, expr), i

    kw = Kws(word)

    if kw is Kws.INT:
        name, i = parse_word(s, i)
        expr, i = extract_from_bounds("=", ";", s, i)
        return DeclareIntInstr(name, expr), i

    elif kw is Kws.PRINT:
        expr, i = extract_from_bounds(" ", ";", s, i)  # todo fix this. it shouldnt rely on " " as the start, it should react to any whitespace char
        return PrintInstr(expr), i

    elif kw is Kws.IF:
        cond, i = extract_from_bounds("(", ")", s, i)
        body, i = extract_from_bounds("{", "}", s, i)
        instrs = parse_instructions(body)
        next_word, next_idx = parse_word(s, i, allow_empty=True)

        if next_word == Kws.ELSE.value:
            else_body, i = extract_from_bounds("{", "}", s, next_idx)
            else_instrs = parse_instructions(else_body)
        else:
            else_instrs = []

        return CondInstr(cond, instrs, else_instrs), i

    elif kw is Kws.WHILE:
        cond, i = extract_from_bounds("(", ")", s, i)
        body, i = extract_from_bounds("{", "}", s, i)
        instrs = parse_instructions(body)
        return LoopInstr(cond, instrs), i

    raise ValueError("Invalid instruction")


def parse_instructions(s):
    instrs = []
    i = 0

    while i < len(s):
        instr, i = parse_instruction(s, i)

        if instr:
            instrs.append(instr)

    return instrs

# # TEST
# txt="""
# int a = 10;
# int b=5;
#
# if(a>b+6){
#   print a;
# }
#
# else {print b+1;}
#
# while(b>0){b=b-1;}
# """
# print(parse_instructions(txt))
