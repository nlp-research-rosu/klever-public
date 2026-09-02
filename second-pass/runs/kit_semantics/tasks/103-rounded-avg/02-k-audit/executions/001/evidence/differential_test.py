#!/usr/bin/env python3
"""Independent differential and exact-contract checks for rounded_avg."""

from __future__ import annotations

import importlib.util
import random
import sys
from fractions import Fraction
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(
    Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution"
)


def exact_contract(n: int, m: int):
    if n > m:
        return -1
    # Average of an inclusive arithmetic progression, with Python's
    # documented nearest/ties-to-even integer rounding applied exactly.
    return bin(round(Fraction(n + m, 2)))


def outcome(function, *args):
    try:
        return ("return", function(*args))
    except Exception as err:  # The exception class is the observable here.
        return ("raise", type(err).__name__)


examples = [
    ((1, 5), "0b11"),
    ((7, 5), -1),
    ((10, 20), "0b1111"),
    ((20, 33), "0b11010"),
]
branch_boundaries = [
    (1, 1),  # n == m and rounded value 1: zero loop iterations
    (1, 2),  # odd sum, lower quotient odd: round upward, value 2
    (2, 2),  # value 2: one loop iteration
    (2, 3),  # odd sum, lower quotient even: round downward
    (3, 4),  # odd sum, lower quotient odd: round upward
    (4, 3),  # n == m + 1: invalid branch boundary
    (3, 4),  # n + 1 == m: closest valid ordering around equality
    (100, 100),
]
outside_contract = [(0, 0), (-2, -2), (-3, 1)]
large_positive = [
    (2**53 - 1, 2**53 - 1),
    (2**53, 2**53),
    (2**53 + 1, 2**53 + 1),
    (2**53 + 2, 2**53 + 3),
    (2**200, 2**200),
    (2**1024, 2**1024),
]

failures: list[str] = []
checked = 0
canonical_mismatches: list[tuple[tuple[int, int], object, object]] = []

for args, expected in examples:
    generated_out = outcome(generated, *args)
    canonical_out = outcome(canonical, *args)
    print(
        f"example args={args} expected={expected!r} "
        f"generated={generated_out} canonical={canonical_out}"
    )
    if generated_out != ("return", expected) or canonical_out != ("return", expected):
        failures.append(f"documented example failed: {args}")

for args in [(), (1,)]:
    generated_out = outcome(generated, *args)
    canonical_out = outcome(canonical, *args)
    print(f"empty/arity args={args} generated={generated_out} canonical={canonical_out}")
    if generated_out != canonical_out or generated_out[0] != "raise":
        failures.append(f"empty/arity behavior differs: {args}")

domain_inputs: list[tuple[int, int]] = list(branch_boundaries)
domain_inputs.extend((n, m) for n in range(1, 81) for m in range(1, 81))
rng = random.Random(103)
domain_inputs.extend(
    (rng.randint(1, 1_000_000), rng.randint(1, 1_000_000))
    for _ in range(4000)
)
for args in domain_inputs:
    expected = exact_contract(*args)
    generated_out = outcome(generated, *args)
    canonical_out = outcome(canonical, *args)
    checked += 1
    if generated_out != ("return", expected):
        failures.append(
            f"generated/exact mismatch args={args}: {generated_out} vs {expected!r}"
        )
    if canonical_out != ("return", expected):
        canonical_mismatches.append((args, canonical_out, expected))

print(
    f"positive representative checks={checked} "
    f"generated_exact_failures={sum('generated/exact' in item for item in failures)} "
    f"canonical_exact_mismatches={len(canonical_mismatches)}"
)
for mismatch in canonical_mismatches[:10]:
    print(f"representative canonical mismatch={mismatch}")

for args in large_positive:
    expected = exact_contract(*args)
    generated_out = outcome(generated, *args)
    canonical_out = outcome(canonical, *args)
    print(
        f"large-positive args-bit-lengths=({args[0].bit_length()},"
        f"{args[1].bit_length()}) generated={generated_out} "
        f"canonical={canonical_out} exact={expected!r}"
    )
    if generated_out != ("return", expected):
        failures.append(f"large generated/exact mismatch: {args}")
    if canonical_out != ("return", expected):
        canonical_mismatches.append((args, canonical_out, expected))

for args in outside_contract:
    print(
        f"outside-contract args={args} generated={outcome(generated, *args)} "
        f"canonical={outcome(canonical, *args)}"
    )

print(f"all_generated_contract_failures={len(failures)}")
print(f"all_canonical_exact_mismatches={len(canonical_mismatches)}")
for failure in failures:
    print(f"FAILURE: {failure}")
sys.exit(1 if failures else 0)
