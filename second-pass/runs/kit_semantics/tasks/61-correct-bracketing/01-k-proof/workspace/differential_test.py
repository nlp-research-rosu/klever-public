import ast
import itertools

from solution import correct_bracketing


def stack_oracle(brackets):
    stack = []
    for bracket in brackets:
        if bracket == "(":
            stack.append(bracket)
        elif stack:
            stack.pop()
        else:
            return False
    return not stack


def target_body(path):
    tree = ast.parse(path.read_text())
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "correct_bracketing"
    )
    return ast.dump(function, include_attributes=False)


if __name__ == "__main__":
    from pathlib import Path

    assert target_body(Path("solution.py")) == target_body(
        Path("concrete_tests.py")
    )

    checked = 0
    for length in range(11):
        for chars in itertools.product("()", repeat=length):
            brackets = "".join(chars)
            expected = stack_oracle(brackets)
            actual = correct_bracketing(brackets)
            assert actual is expected, (brackets, actual, expected)
            checked += 1
    print(f"checked={checked} mismatches=0")
