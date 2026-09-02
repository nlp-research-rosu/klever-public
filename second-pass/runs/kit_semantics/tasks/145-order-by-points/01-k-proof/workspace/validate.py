import ast
import itertools
from pathlib import Path
import random

from solution import digit_sum, order_by_points


solution_tree = ast.parse(Path("solution.py").read_text(encoding="utf-8"))
concrete_tree = ast.parse(Path("concrete_tests.py").read_text(encoding="utf-8"))
assert ast.dump(solution_tree) == ast.dump(
    ast.Module(body=concrete_tree.body[:2], type_ignores=[])
)


def oracle_digit_sum(number):
    text = str(number)
    if text[0] == "-":
        return -int(text[1]) + sum(int(char) for char in text[2:])
    return sum(int(char) for char in text)


scalar_cases = 0
for value in range(-10000, 10001):
    assert digit_sum(value) == oracle_digit_sum(value)
    scalar_cases += 1

list_cases = 0
pool = [-101, -20, -12, -11, -1, 0, 1, 2, 10, 11, 12, 20, 101]
for length in range(5):
    for values in itertools.product(pool[:5], repeat=length):
        expected = sorted(values, key=oracle_digit_sum)
        assert order_by_points(list(values)) == list(expected)
        list_cases += 1

rng = random.Random(20260725)
for _ in range(1000):
    values = [rng.randint(-10**12, 10**12) for _ in range(rng.randrange(0, 30))]
    expected = sorted(values, key=oracle_digit_sum)
    assert order_by_points(values) == expected
    list_cases += 1

print(
    "validated exact concrete-test body identity, "
    f"{scalar_cases} digit keys, and {list_cases} stable sorts"
)
