#!/usr/bin/env python3
"""Independent differential and contract-property checks for find_zero."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import signal
from typing import Callable


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


trusted = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated = load_module(
    "generated_solution", Path("/tmp/audit-work/32-find-zero/solution.py")
)


def poly(coefficients: list[int], x: float) -> float:
    return math.fsum(
        coefficient * math.pow(x, exponent)
        for exponent, coefficient in enumerate(coefficients)
    )


fixed_cases: list[tuple[str, list[int]]] = [
    ("prompt-linear", [1, 2]),
    ("prompt-cubic-three-roots", [-6, 11, -6, 1]),
    ("minimum-root-at-zero", [0, 1]),
    ("left-endpoint-root", [1, 1]),
    ("right-endpoint-root", [-1, 1]),
    ("one-bracket-expansion-positive", [-2, 1]),
    ("one-bracket-expansion-negative", [2, 1]),
    ("multiple-expansions-positive", [-8, 0, 0, 1]),
    ("multiple-expansions-negative", [8, 0, 0, 1]),
    ("flat-simple-root", [0, 0, 0, 1]),
    ("degree-five", [-7, 3, -2, 5, 0, 1]),
    ("small-leading-coefficient", [8, 0, 0, -1]),
]

rng = random.Random(320032)
generated_cases: list[list[int]] = []
for _ in range(180):
    length = rng.choice((2, 4, 6))
    coefficients = [rng.randint(-8, 8) for _ in range(length)]
    while coefficients[-1] == 0:
        coefficients[-1] = rng.randint(-8, 8)
    generated_cases.append(coefficients)

all_cases = fixed_cases + [
    (f"generated-{index:03d}", coefficients)
    for index, coefficients in enumerate(generated_cases)
]

exact_result_differences = 0
material_result_differences: list[tuple[str, list[int], float, float]] = []
nonfinite_results: list[tuple[str, list[int], float, float]] = []
worst_delta = (0.0, "", [])
worst_generated_residual = (0.0, "", [])
worst_trusted_residual = (0.0, "", [])

for label, coefficients in all_cases:
    trusted_result = trusted.find_zero(coefficients)
    generated_result = generated.find_zero(coefficients)
    if trusted_result != generated_result:
        exact_result_differences += 1
    if not (math.isfinite(trusted_result) and math.isfinite(generated_result)):
        nonfinite_results.append(
            (label, coefficients, trusted_result, generated_result)
        )
        continue
    delta = abs(trusted_result - generated_result)
    if delta > worst_delta[0]:
        worst_delta = (delta, label, coefficients)
    relative_scale = max(1.0, abs(trusted_result), abs(generated_result))
    if delta > 1.1e-10 * relative_scale:
        material_result_differences.append(
            (label, coefficients, trusted_result, generated_result)
        )
    trusted_residual = abs(poly(coefficients, trusted_result))
    generated_residual = abs(poly(coefficients, generated_result))
    if trusted_residual > worst_trusted_residual[0]:
        worst_trusted_residual = (trusted_residual, label, coefficients)
    if generated_residual > worst_generated_residual[0]:
        worst_generated_residual = (generated_residual, label, coefficients)


def timed_call(function: Callable[[list[int]], float], value: list[int]):
    def alarm_handler(_signum, _frame):
        raise TimeoutError("one-second timeout")

    old_handler = signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(1)
    try:
        return ("returned", function(value))
    except TimeoutError:
        return ("timeout", None)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


out_of_domain = {
    "empty": {
        "trusted": timed_call(trusted.find_zero, []),
        "generated": timed_call(generated.find_zero, []),
    },
    "positive-constant": {
        "trusted": timed_call(trusted.find_zero, [1]),
        "generated": timed_call(generated.find_zero, [1]),
    },
    "zero-leading-coefficient": {
        "trusted": timed_call(trusted.find_zero, [1, 0]),
        "generated": timed_call(generated.find_zero, [1, 0]),
    },
}

serialized_generated = json.dumps(
    generated_cases, separators=(",", ":"), sort_keys=False
).encode()
print(f"fixed_cases={len(fixed_cases)} generated_cases={len(generated_cases)}")
print(
    "generated_inputs_sha256="
    + hashlib.sha256(serialized_generated).hexdigest()
)
for label, coefficients in fixed_cases:
    trusted_result = trusted.find_zero(coefficients)
    generated_result = generated.find_zero(coefficients)
    print(
        f"FIXED {label} xs={coefficients} "
        f"trusted={trusted_result:.17g} generated={generated_result:.17g} "
        f"delta={abs(trusted_result-generated_result):.17g} "
        f"trusted_residual={abs(poly(coefficients, trusted_result)):.17g} "
        f"generated_residual={abs(poly(coefficients, generated_result)):.17g}"
    )
print(f"exact_result_differences={exact_result_differences}")
print(f"material_result_differences={len(material_result_differences)}")
print(f"nonfinite_results={len(nonfinite_results)}")
print(
    f"worst_delta={worst_delta[0]:.17g} "
    f"case={worst_delta[1]} xs={worst_delta[2]}"
)
print(
    f"worst_trusted_residual={worst_trusted_residual[0]:.17g} "
    f"case={worst_trusted_residual[1]} xs={worst_trusted_residual[2]}"
)
print(
    f"worst_generated_residual={worst_generated_residual[0]:.17g} "
    f"case={worst_generated_residual[1]} xs={worst_generated_residual[2]}"
)
print(f"out_of_domain={out_of_domain}")

assert not material_result_differences
assert not nonfinite_results
print("DIFFERENTIAL_OK")
