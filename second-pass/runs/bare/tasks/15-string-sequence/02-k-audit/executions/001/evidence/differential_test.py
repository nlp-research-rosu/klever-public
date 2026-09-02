#!/usr/bin/env python3
"""Independent differential test for HumanEval 15 string_sequence."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/tmp/audit-work/rebuild/solution.py"), "candidate_solution")

# Documented examples, both sides of the negative branch, the loop's
# zero/one/multiple-iteration boundaries, powers-of-ten string boundaries,
# an exhaustive small interval, and deterministic generated integers.
documented = [0, 5]
boundaries = [-100, -2, -1, 0, 1, 2, 5, 9, 10, 11, 98, 99, 100, 101, 999]
exhaustive = list(range(-128, 257))
rng = random.Random(150015)
generated_inputs = [rng.randint(-1000, 1000) for _ in range(500)]
inputs = list(dict.fromkeys(documented + boundaries + exhaustive + generated_inputs))

mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"documented={documented}")
print(f"boundaries={boundaries}")
print("exhaustive_range=[-128, 256]")
print("generated_seed=150015 generated_count=500 generated_range=[-1000, 1000]")
print(f"unique_inputs={len(inputs)}")
print(f"mismatches={len(mismatches)}")
for item in mismatches[:20]:
    print(f"MISMATCH {item!r}")

raise SystemExit(1 if mismatches else 0)
