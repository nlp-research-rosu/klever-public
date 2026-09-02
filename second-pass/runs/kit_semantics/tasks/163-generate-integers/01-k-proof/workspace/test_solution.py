import ast

from solution import generate_integers


def oracle(a, b):
    low = min(a, b)
    high = max(a, b)
    return [
        value
        for value in range(low, high + 1)
        if value < 10 and value % 2 == 0
    ]


def function_ast(path):
    with open(path, encoding="utf-8") as source_file:
        module = ast.parse(source_file.read(), filename=path)
    return ast.dump(module.body[0], include_attributes=False)


assert function_ast("solution.py") == function_ast("concrete-tests.py")

checked = 0
for first in range(1, 101):
    for second in range(1, 101):
        actual = generate_integers(first, second)
        expected = oracle(first, second)
        assert actual == expected, (first, second, actual, expected)
        checked += 1

print(f"PASS: {checked} positive-input pairs; 0 mismatches")
