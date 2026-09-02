import importlib.util
import math
import random


candidate_spec = importlib.util.spec_from_file_location("candidate", "solution.py")
candidate = importlib.util.module_from_spec(candidate_spec)
candidate_spec.loader.exec_module(candidate)


def oracle_poly(xs, x):
    return sum(coeff * (x ** index) for index, coeff in enumerate(xs))


assert round(candidate.find_zero([1, 2]), 2) == -0.5
assert round(candidate.find_zero([-6, 11, -6, 1]), 2) == 1.0

random.seed(20260729)
for case in range(500):
    size = random.choice((2, 4, 6, 8))
    coefficients = [random.uniform(-5.0, 5.0) for _ in range(size)]
    while abs(coefficients[-1]) < 0.25:
        coefficients[-1] = random.uniform(-5.0, 5.0)

    root = candidate.find_zero(coefficients)
    residual = abs(oracle_poly(coefficients, root))
    scale = 1.0 + sum(
        abs(coeff * (root ** index))
        for index, coeff in enumerate(coefficients)
    )
    assert math.isfinite(root)
    assert residual / scale < 1e-8, (
        case,
        coefficients,
        root,
        residual / scale,
    )

print("500 randomized odd-degree cases passed normalized residual < 1e-8")
