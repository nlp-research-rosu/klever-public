#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test for 63-fibfib."""

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
    return module.fibfib


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/reference-src/canonical.py")
)
generated = load_entry(
    "submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

# Prompt examples, the empty/zero-iteration case, each canonical branch
# boundary, a dense prefix, and a reproducible generated sample.
documented_examples = [1, 5, 8]
empty_and_boundaries = [0, 1, 2, 3, 4]
dense_prefix = list(range(0, 16))
seed = 630063
rng = random.Random(seed)
generated_inputs = [rng.randint(0, 20) for _ in range(20)]
representative_larger = [18, 20, 22]

ordered_inputs: list[int] = []
for value in (
    documented_examples
    + empty_and_boundaries
    + dense_prefix
    + generated_inputs
    + representative_larger
):
    if value not in ordered_inputs:
        ordered_inputs.append(value)

print(f"documented_examples={documented_examples}")
print(f"empty_and_boundaries={empty_and_boundaries}")
print(f"dense_prefix={dense_prefix}")
print(f"generated_seed={seed}")
print(f"generated_inputs={generated_inputs}")
print(f"representative_larger={representative_larger}")
print(f"unique_inputs={ordered_inputs}")

mismatches = []
for n in ordered_inputs:
    expected = canonical(n)
    actual = generated(n)
    equal = expected == actual
    print(f"n={n} canonical={expected} generated={actual} equal={equal}")
    if not equal:
        mismatches.append((n, expected, actual))

print(f"cases={len(ordered_inputs)} mismatches={len(mismatches)}")
if mismatches:
    print(f"mismatch_details={mismatches}")
    raise SystemExit(1)
