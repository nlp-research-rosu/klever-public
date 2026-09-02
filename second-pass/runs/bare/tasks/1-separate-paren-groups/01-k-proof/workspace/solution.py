from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    result = []
    current = ""
    depth = 0
    ch = ""
    for ch in paren_string:
        if ch != " ":
            current += ch
            if ch == "(":
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    result.append(current)
                    current = ""
    return result
