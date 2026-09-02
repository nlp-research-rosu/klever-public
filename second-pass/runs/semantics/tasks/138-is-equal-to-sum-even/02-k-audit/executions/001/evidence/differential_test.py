#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py versus solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_equal_to_sum_even


def outcome(function: Callable[..., Any], *args: Any) -> tuple[str, Any]:
    try:
        value = function(*args)
        return ("return", (type(value).__name__, value))
    except Exception as error:  # Differentially compare the arity boundary too.
        return ("raise", (type(error).__name__, str(error)))


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_138")
generated = load_entry(
    Path("/tmp/audit-work/review-138/solution.py"), "candidate_solution_138"
)

# Examples plus exact truth-value branch boundaries and representative integers.
documented = [4, 6, 8]
boundaries = [
    -(10**100),
    -257,
    -256,
    -9,
    -8,
    -7,
    -2,
    -1,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    255,
    256,
    257,
    10**100 - 1,
    10**100,
]
exhaustive_small = list(range(-256, 257))

rng = random.Random(138)
generated_inputs: list[int] = []
for _ in range(500):
    magnitude = rng.getrandbits(rng.randrange(0, 513))
    generated_inputs.append(-magnitude if rng.randrange(2) else magnitude)

inputs = list(dict.fromkeys(documented + boundaries + exhaustive_small + generated_inputs))
mismatches: list[tuple[int, tuple[str, Any], tuple[str, Any]]] = []
for value in inputs:
    expected = outcome(canonical, value)
    actual = outcome(generated, value)
    if expected != actual:
        mismatches.append((value, expected, actual))

# "Empty" call boundary: neither one-argument entry point accepts zero arguments.
empty_expected = outcome(canonical)
empty_actual = outcome(generated)
if empty_expected != empty_actual:
    mismatches.append(("<no argument>", empty_expected, empty_actual))  # type: ignore[arg-type]

print(f"documented={documented}")
print(f"boundaries={boundaries}")
print("exhaustive_small=range(-256, 257)")
print("generated_seed=138 generated_count=500 generated_bits=0..512 signed")
print(f"unique_integer_inputs={len(inputs)}")
print(f"empty_call_expected={empty_expected}")
print(f"empty_call_actual={empty_actual}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
