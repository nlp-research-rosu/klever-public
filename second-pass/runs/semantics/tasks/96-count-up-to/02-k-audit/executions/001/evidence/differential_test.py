#!/usr/bin/env python3
"""Independent differential check for HumanEval problem 96."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/96-count-up-to/source/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_up_to


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_96")
generated = load_entry(GENERATED_PATH, "generated_solution_96")

examples = {
    5: [2, 3],
    11: [2, 3, 5, 7],
    0: [],
    20: [2, 3, 5, 7, 11, 13, 17, 19],
    1: [],
    18: [2, 3, 5, 7, 11, 13, 17],
}

# 0..5 covers the empty-result boundary, the skipped inner loop for candidate
# 2, the first append, and the first composite. The exhaustive prefix exercises
# every later conditional shape many times.
inputs = list(range(0, 151))
inputs.extend([151, 173, 199, 200, 251, 257, 300, 397, 400])
rng = random.Random(960024)
inputs.extend(rng.randrange(0, 401) for _ in range(40))
inputs = list(dict.fromkeys(inputs))

mismatches = []
for n in inputs:
    canonical_result = canonical(n)
    generated_result = generated(n)
    if canonical_result != generated_result:
        mismatches.append((n, canonical_result, generated_result))

for n, expected in examples.items():
    canonical_result = canonical(n)
    generated_result = generated(n)
    if canonical_result != expected or generated_result != expected:
        mismatches.append(
            (f"example:{n}", expected, canonical_result, generated_result)
        )

print(f"CANONICAL={CANONICAL_PATH}")
print(f"GENERATED={GENERATED_PATH}")
print("DOMAIN=non-negative Python integers")
print(f"INPUT_COUNT={len(inputs)}")
print(f"INPUTS={inputs}")
print(f"DOCUMENTED_EXAMPLES={examples}")
print(f"MISMATCH_COUNT={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH={mismatch!r}")

raise SystemExit(1 if mismatches else 0)
