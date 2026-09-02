from typing import List


# Kept textually identical to the submitted solution; the AST identity check in
# the logged test command excludes these assertions before comparing functions.
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


assert parse_nested_parens('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
assert parse_nested_parens('') == [0]
assert parse_nested_parens(' ()') == [0, 1]
assert parse_nested_parens('() ') == [1, 0]
assert parse_nested_parens('()  ()') == [1, 0, 1]
assert parse_nested_parens('(())()') == [2]
