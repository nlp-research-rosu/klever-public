from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    depths = []
    depth = 0
    deepest = 0
    char = ""

    for char in paren_string:
        if char == "(":
            depth += 1
            if depth > deepest:
                deepest = depth
        elif char == ")":
            depth -= 1
        elif deepest > 0:
            depths.append(deepest)
            deepest = 0

    if deepest > 0:
        depths.append(deepest)

    return depths
