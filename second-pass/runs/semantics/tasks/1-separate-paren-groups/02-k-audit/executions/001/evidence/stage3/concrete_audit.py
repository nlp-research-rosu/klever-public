from typing import List


# Exact submitted function body, followed by reviewer-selected assertions.
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


assert separate_paren_groups("") == []
assert separate_paren_groups("   ") == []
assert separate_paren_groups("()") == ["()"]
assert separate_paren_groups("(())") == ["(())"]
assert separate_paren_groups("()()") == ["()", "()"]
assert separate_paren_groups("( ) (( )) (( )( ))") == ["()", "(())", "(()())"]
assert separate_paren_groups("  (()())() ") == ["(()())", "()"]
assert separate_paren_groups("(((())))") == ["(((())))"]
