def separate_paren_groups(paren_string):
    result = []
    current = ""
    depth = 0
    c = ""
    for c in paren_string:
        if c == "(":
            current = current + c
            depth = depth + 1
        elif c == ")":
            current = current + c
            depth = depth - 1
            if depth == 0:
                result = result + [current]
                current = ""
    return result
