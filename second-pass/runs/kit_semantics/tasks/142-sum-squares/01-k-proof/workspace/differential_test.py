import ast
import itertools

from solution import sum_squares


def oracle(values):
    total = 0
    for position, value in enumerate(values):
        if position % 3 == 0:
            total += value ** 2
        elif position % 4 == 0:
            total += value ** 3
        else:
            total += value
    return total


def function_ast(path):
    with open(path, encoding="utf-8") as source:
        module = ast.parse(source.read(), filename=path)
    function = next(node for node in module.body if isinstance(node, ast.FunctionDef))
    return ast.dump(function, include_attributes=False)


assert function_ast("solution.py") == function_ast("concrete-smoke.py")

checked = 0
mismatches = 0
for length in range(6):
    for values in itertools.product(range(-3, 4), repeat=length):
        checked += 1
        if sum_squares(list(values)) != oracle(values):
            mismatches += 1

print(f"cases={checked} mismatches={mismatches} smoke_body_matches_solution=yes")
assert mismatches == 0
