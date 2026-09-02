from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    result = []
    depth = 0
    maximum = 0
    char = ''

    for char in paren_string:
        if char == '(':
            depth += 1
            if depth > maximum:
                maximum = depth
        elif char == ')':
            depth -= 1
        elif char == ' ':
            result.append(maximum)
            depth = 0
            maximum = 0

    result.append(maximum)
    return result
