from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    groups = []
    current = ""
    depth = 0

    for character in paren_string:
        if character == " ":
            continue

        current += character
        if character == "(":
            depth += 1
        else:
            depth -= 1

        if depth == 0:
            groups.append(current)
            current = ""

    return groups
