#!/usr/bin/env python3
"""Independent differential checks for HumanEval/76.

The trusted canonical and scratch-reconstructed candidate are imported from
explicit paths.  The multiplication oracle does not reuse the candidate's
division algorithm or the K proof equations.
"""

from __future__ import annotations

import importlib.util
import random
import signal
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/76-is-simple-power")


def import_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


canonical = import_entry("trusted_canonical_76", SCRATCH / "trusted/canonical.py")
generated = import_entry("generated_solution_76", SCRATCH / "solution.py")


class CallTimedOut(Exception):
    pass


def _timeout(_signum, _frame):
    raise CallTimedOut


def bounded_call(function, x: int, n: int, seconds: float = 0.02):
    previous = signal.signal(signal.SIGALRM, _timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return ("return", function(x, n))
    except CallTimedOut:
        return ("timeout", None)
    except BaseException as error:  # Preserve unexpected canonical behavior.
        return ("exception", f"{type(error).__name__}: {error}")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def multiplication_oracle(x: int, n: int) -> bool:
    """Whether x = n**e for some integer e >= 0."""
    if x == 1:
        return True
    if n == 0:
        return x == 0
    if n == 1:
        return False
    if n == -1:
        return x == -1
    power = 1
    limit = abs(x)
    while abs(power) <= limit:
        if power == x:
            return True
        power *= n
    return False


documented = [(1, 4), (2, 2), (8, 2), (3, 2), (3, 1), (5, 3)]
branch_boundaries = [
    (1, 0),
    (1, 1),
    (1, -1),
    (1, -2),
    (0, 0),
    (-1, 0),
    (2, 0),
    (0, 1),
    (2, 1),
    (-1, -1),
    (2, -1),
    (0, 2),
    (0, -2),
    (8, 2),
    (12, 2),
    (-8, -2),
    (16, -2),
    (8, -2),
    (-8, 2),
]
power_boundaries = []
for base in (-5, -2, 2, 3, 10):
    for exponent in range(0, 9):
        value = base**exponent
        power_boundaries.extend(
            [(value, base), (value - 1, base), (value + 1, base)]
        )

positive_grid = [(x, n) for x in range(0, 201) for n in range(1, 21)]
broad_grid = [(x, n) for x in range(-40, 81) for n in range(-5, 6)]
rng = random.Random(76076)
random_cases = [
    (rng.randint(-100_000, 100_000), rng.randint(-20, 20))
    for _ in range(1_000)
]

all_cases = sorted(
    set(documented + branch_boundaries + power_boundaries + positive_grid + broad_grid + random_cases)
)

generated_oracle_mismatches = []
canonical_generated_divergences = []
canonical_timeouts = []
canonical_exceptions = []
for x, n in all_cases:
    actual = generated(x, n)
    expected = multiplication_oracle(x, n)
    if actual != expected:
        generated_oracle_mismatches.append((x, n, actual, expected))
    canonical_outcome = bounded_call(canonical, x, n)
    if canonical_outcome[0] == "return":
        if canonical_outcome[1] != actual:
            canonical_generated_divergences.append(
                (x, n, canonical_outcome[1], actual, expected)
            )
    elif canonical_outcome[0] == "timeout":
        canonical_timeouts.append((x, n))
    else:
        canonical_exceptions.append((x, n, canonical_outcome[1]))

positive_mismatches = []
for x, n in positive_grid:
    c = canonical(x, n)
    g = generated(x, n)
    if c != g:
        positive_mismatches.append((x, n, c, g))

print("contract_interpretation: exponent is an integer e >= 0")
print("empty_case: not applicable; the entry point accepts two integers")
print(f"documented_cases={len(documented)}")
print(f"branch_boundary_cases={len(branch_boundaries)}")
print(f"positive_grid_cases={len(positive_grid)}")
print(f"broad_grid_cases={len(broad_grid)}")
print(f"random_cases={len(random_cases)} seed=76076")
print(f"unique_total_cases={len(all_cases)}")
print(f"generated_oracle_mismatches={len(generated_oracle_mismatches)}")
print(f"positive_canonical_generated_mismatches={len(positive_mismatches)}")
print(f"canonical_generated_divergences={len(canonical_generated_divergences)}")
print(f"canonical_timeouts={len(canonical_timeouts)}")
print(f"canonical_exceptions={len(canonical_exceptions)}")
print(
    "canonical_generated_divergence_examples="
    + repr(canonical_generated_divergences[:20])
)
print("canonical_timeout_examples=" + repr(canonical_timeouts[:20]))
print("generated_oracle_mismatch_examples=" + repr(generated_oracle_mismatches[:20]))
print("positive_mismatch_examples=" + repr(positive_mismatches[:20]))

if generated_oracle_mismatches or positive_mismatches or canonical_exceptions:
    raise SystemExit(1)
