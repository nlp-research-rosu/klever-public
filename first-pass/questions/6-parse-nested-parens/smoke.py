def parse_nested_parens(paren_string):
    result = []
    depth = 0
    curmax = 0
    has = False
    c = ""
    for c in paren_string + ' ':
        if c == '(':
            depth = depth + 1
            if depth > curmax:
                curmax = depth
            has = True
        else:
            if c == ' ':
                if has:
                    result = result + [curmax]
                    depth = 0
                    curmax = 0
                    has = False
            else:
                depth = depth - 1
                has = True
    return result


# Smoke check from the prompt docstring (NOT a hidden test).
assert parse_nested_parens('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
