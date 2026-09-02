#!/usr/bin/env python3
import ast
import re
from pathlib import Path


def primes_below(limit: int) -> list[int]:
    result = []
    for value in range(2, limit):
        if all(value % divisor for divisor in range(2, int(value**0.5) + 1)):
            result.append(value)
    return result


primes = primes_below(100)
triple_products = sorted(
    {
        p * q * r
        for p in primes
        for q in primes
        for r in primes
        if p * q * r < 100
    }
)

solution_text = Path("/reference/k-proof/solution.py").read_text()
solution_tree = ast.parse(solution_text)
function = next(node for node in solution_tree.body if isinstance(node, ast.FunctionDef))
return_node = next(node for node in ast.walk(function) if isinstance(node, ast.Return))
solution_constants = sorted(
    {
        comparator.value
        for node in ast.walk(return_node.value)
        if isinstance(node, ast.Compare)
        for comparator in node.comparators
        if isinstance(comparator, ast.Constant) and isinstance(comparator.value, int)
    }
)

spec_text = Path("/reference/k-proof/spec.k").read_text()
postcondition = spec_text.split("=>", 1)[1].split("</k>", 1)[0]
postcondition_constants = [
    int(value) for value in re.findall(r"A\s*==Int\s*(-?\d+)", postcondition)
]

print("independent_triple_prime_products_under_100=", triple_products)
print("solution_disjunction_constants=", solution_constants)
print("spec_postcondition_constants=", postcondition_constants)
print("solution_matches_math=", solution_constants == triple_products)
print("postcondition_matches_solution=", postcondition_constants == solution_constants)
for value in (-101, -1, 0, 1, 7, 8, 12, 30, 64, 97, 98, 99):
    print(f"witness {value}: expected={value in triple_products} frozen_result={value in solution_constants}")
if solution_constants != triple_products or postcondition_constants != solution_constants:
    raise SystemExit(1)
