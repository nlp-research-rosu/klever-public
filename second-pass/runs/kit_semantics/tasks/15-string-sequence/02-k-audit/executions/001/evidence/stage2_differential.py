#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry("audited_candidate", Path("/candidate/solution.py"))

# Examples, negative/empty-range behavior, the if boundary, loop zero/one/many
# iterations, decimal-width boundaries, and larger values.
named_cases = {
    "documented_zero": 0,
    "documented_five": 5,
    "negative_far": -25,
    "negative_minus_two": -2,
    "if_boundary_negative": -1,
    "if_boundary_nonnegative": 0,
    "one_loop_iteration": 1,
    "two_loop_iterations": 2,
    "single_to_double_digits_left": 9,
    "single_to_double_digits_right": 10,
    "double_to_triple_digits_left": 99,
    "double_to_triple_digits_right": 100,
    "larger": 999,
}

# Full small neighborhood plus reproducible representative generated integers.
small_exhaustive = list(range(-100, 301))
rng = random.Random(150029)
generated = [rng.randint(-5000, 5000) for _ in range(500)]
all_inputs = list(dict.fromkeys([*named_cases.values(), *small_exhaustive, *generated]))

mismatches = []
exceptions = []
for n in all_inputs:
    try:
        expected = canonical(n)
    except Exception as error:  # pragma: no cover - evidence path
        exceptions.append((n, "canonical", type(error).__name__, str(error)))
        continue
    try:
        actual = candidate(n)
    except Exception as error:  # pragma: no cover - evidence path
        exceptions.append((n, "candidate", type(error).__name__, str(error)))
        continue
    if actual != expected:
        mismatches.append((n, expected, actual))

print("oracle=/reference/canonical.py:string_sequence")
print("candidate=/candidate/solution.py:string_sequence")
print(f"named_cases={named_cases}")
for name, n in named_cases.items():
    print(
        f"named_result[{name}] n={n} "
        f"canonical={canonical(n)!r} candidate={candidate(n)!r}"
    )
print(f"small_exhaustive=range(-100,301) count={len(small_exhaustive)}")
print(f"generated_seed=150029 generated_count={len(generated)}")
print(f"generated_inputs={generated}")
print(f"unique_inputs={len(all_inputs)}")
print(f"exceptions={exceptions}")
print(f"mismatches={mismatches}")

if exceptions or mismatches:
    raise SystemExit(1)
