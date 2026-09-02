import ast
import random

from solution import rescale_to_unit


def oracle(numbers):
    ordered = sorted(numbers)
    low = ordered[0]
    high = ordered[-1]
    return [(number - low) / (high - low) for number in numbers]


def function_body(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    function = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef)
    )
    return ast.dump(ast.Module(body=function.body, type_ignores=[]))


assert function_body("solution.py") == function_body("concrete_test.py")

rng = random.Random(20260729)
cases = [[1.0, 2.0, 3.0, 4.0, 5.0]]
while len(cases) < 1001:
    length = rng.randint(2, 20)
    numbers = [rng.randint(-200, 200) / 4.0 for _ in range(length)]
    if min(numbers) != max(numbers):
        cases.append(numbers)

mismatches = []
for numbers in cases:
    actual = rescale_to_unit(numbers)
    expected = oracle(numbers)
    if actual != expected:
        mismatches.append((numbers, actual, expected))

assert not mismatches, mismatches[:1]
print("ast-body-match: yes")
print(f"cpython-differential: {len(cases)} cases, 0 mismatches")
