from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    groups = []
    current = ""
    depth = 0
    char = ""
    for char in paren_string:
        if char != " ":
            current += char
            if char == "(":
                depth += 1
            else:
                depth -= 1
            if depth == 0:
                groups.append(current)
                current = ""
    return groups


assert separate_paren_groups("( ) (( )) (( )( ))") == [
    "()",
    "(())",
    "(()())",
]
assert separate_paren_groups("()()") == ["()", "()"]
assert separate_paren_groups("(((())))") == ["(((())))"]
assert separate_paren_groups("   ") == []
