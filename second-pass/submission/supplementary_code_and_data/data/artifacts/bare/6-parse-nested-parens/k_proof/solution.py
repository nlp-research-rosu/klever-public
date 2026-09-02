from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    result = []
    groups = paren_string.split(" ")
    for group in groups:
        depth = 0
        maximum = 0
        for character in group:
            if character == "(":
                depth += 1
                if depth > maximum:
                    maximum = depth
            else:
                depth -= 1
        result.append(maximum)
    return result
