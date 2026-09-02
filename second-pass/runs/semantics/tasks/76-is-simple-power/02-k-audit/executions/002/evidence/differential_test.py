#!/usr/bin/env python3
"""Independent differential checks for HumanEval/76.

The trusted canonical and generated implementation are imported from explicit
paths.  A small mathematical oracle checks existence of a nonnegative integer
exponent for integer bases and results.
"""

from __future__ import annotations

import importlib.util
import random
import signal
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable


class EvaluationTimeout(Exception):
    pass


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def alarm_handler(_signum: int, _frame: object) -> None:
    raise EvaluationTimeout


signal.signal(signal.SIGALRM, alarm_handler)


def timed_call(function: Callable[[int, int], bool], x: int, n: int) -> object:
    signal.setitimer(signal.ITIMER_REAL, 0.02)
    try:
        return function(x, n)
    except EvaluationTimeout:
        return "TIMEOUT"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)


def nonnegative_integer_power(x: int, n: int) -> bool:
    """Whether n**k == x for some integer k >= 0."""
    if x == 1:
        return True
    if n == 0:
        return x == 0
    if n == 1:
        return False
    if n == -1:
        return x == -1
    if x == 0:
        return False
    value = 1
    while abs(value) <= abs(x):
        value *= n
        if value == x:
            return True
    return False


if len(sys.argv) != 3:
    raise SystemExit("usage: differential_test.py TRUSTED_CANONICAL GENERATED_SOLUTION")

canonical = load_module("trusted_canonical", Path(sys.argv[1]))
generated = load_module("generated_solution", Path(sys.argv[2]))

documented = [
    (1, 4, True),
    (2, 2, True),
    (8, 2, True),
    (3, 2, False),
    (3, 1, False),
    (5, 3, False),
]
boundaries = [
    (-1, -2),
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (-1, 2),
    (0, -2),
    (0, -1),
    (0, 0),
    (0, 1),
    (0, 2),
    (1, -2),
    (1, -1),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, -2),
    (2, -1),
    (2, 0),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, -2),
    (4, 2),
    (8, 2),
    (9, 3),
    (16, 2),
    (16, 4),
    (64, 4),
    (128, 4),
]

rng = random.Random(760076)
generated_positive = [(rng.randint(1, 10000), rng.randint(1, 50)) for _ in range(500)]
positive_domain = (
    [(x, n) for x in range(1, 401) for n in range(1, 31)]
    + generated_positive
    + [(x, n) for x, n, _expected in documented]
)
integer_grid = [(x, n) for x in range(-32, 65) for n in range(-5, 9)]

for x, n, expected in documented:
    got_generated = generated.is_simple_power(x, n)
    got_canonical = timed_call(canonical.is_simple_power, x, n)
    assert got_generated is expected, (x, n, got_generated, expected)
    assert got_canonical is expected, (x, n, got_canonical, expected)
print(f"documented_examples_passed={len(documented)}")

positive_mismatches: list[tuple[int, int, object, object, bool]] = []
for x, n in positive_domain:
    got_generated = generated.is_simple_power(x, n)
    got_canonical = timed_call(canonical.is_simple_power, x, n)
    oracle = nonnegative_integer_power(x, n)
    if got_generated != got_canonical or got_generated != oracle:
        positive_mismatches.append((x, n, got_generated, got_canonical, oracle))
print(f"positive_domain_cases={len(positive_domain)}")
print(f"positive_domain_mismatches={len(positive_mismatches)}")
for mismatch in positive_mismatches[:40]:
    print(f"positive_mismatch={mismatch!r}")

grid_generated_canonical: list[tuple[int, int, object, object]] = []
grid_generated_oracle: list[tuple[int, int, object, bool]] = []
canonical_timeouts: list[tuple[int, int]] = []
for x, n in integer_grid:
    got_generated = generated.is_simple_power(x, n)
    got_canonical = timed_call(canonical.is_simple_power, x, n)
    oracle = nonnegative_integer_power(x, n)
    if got_canonical == "TIMEOUT":
        canonical_timeouts.append((x, n))
    elif got_generated != got_canonical:
        grid_generated_canonical.append((x, n, got_generated, got_canonical))
    if got_generated != oracle:
        grid_generated_oracle.append((x, n, got_generated, oracle))

print(f"integer_grid_cases={len(integer_grid)}")
print(f"integer_grid_canonical_timeouts={len(canonical_timeouts)}")
print(f"integer_grid_generated_canonical_mismatches={len(grid_generated_canonical)}")
for mismatch in grid_generated_canonical[:40]:
    print(f"generated_canonical_mismatch={mismatch!r}")
print(f"integer_grid_generated_math_mismatches={len(grid_generated_oracle)}")
for mismatch in grid_generated_oracle[:40]:
    print(f"generated_math_mismatch={mismatch!r}")

print("boundary_results:")
for x, n in boundaries:
    print(
        f"  x={x} n={n} generated={generated.is_simple_power(x, n)!r} "
        f"canonical={timed_call(canonical.is_simple_power, x, n)!r} "
        f"math={nonnegative_integer_power(x, n)!r}"
    )

assert not positive_mismatches
print("RESULT: positive-integer differential PASS; unrestricted-integer results reported above")
