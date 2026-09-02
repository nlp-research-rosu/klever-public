#!/usr/bin/env python3
"""Independent differential test for HumanEval problem 147."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path

REFERENCE = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/audit147/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


canonical = load_entry(REFERENCE, "trusted_canonical")
generated = load_entry(GENERATED, "candidate_generated")

# Includes the documented example, the empty-array extension, the smallest
# legal values, the first possible triple, every residue transition through
# n=12, and values on both sides of larger multiples of three.
directed = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 29, 30, 31, 59, 60, 61]

# The canonical implementation is cubic, so keep its independently generated
# sample bounded while still covering all residue classes repeatedly.
rng = random.Random(147)
generated_inputs = [rng.randint(1, 120) for _ in range(40)]
exhaustive_small = list(range(0, 81))
inputs = list(dict.fromkeys(directed + exhaustive_small + generated_inputs))

mismatches: list[tuple[int, int, int]] = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"oracle={REFERENCE}")
print(f"generated={GENERATED}")
print("formal_intended_domain=positive integers n >= 1")
print("extra_boundary_extension=n=0")
print(f"documented_example n=5 canonical={canonical(5)} generated={generated(5)}")
print(f"directed_inputs={directed}")
print(f"seed=147 generated_inputs={generated_inputs}")
print(f"unique_input_count={len(inputs)} min={min(inputs)} max={max(inputs)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches:
        print(f"MISMATCH n={mismatch[0]} canonical={mismatch[1]} generated={mismatch[2]}")
    raise SystemExit(1)
print("RESULT=PASS")
