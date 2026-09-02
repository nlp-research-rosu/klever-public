#!/usr/bin/env python3
"""Independent differential check for HumanEval/36.

Oracle: /reference/canonical.py, loaded directly from the trusted mount.
Candidate: the clean scratch copy of /candidate/solution.py.
No K summary function or proof equation is reused here.
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_entry("trusted_humaneval36", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_humaneval36", Path("/tmp/audit-work/source/solution.py")
)

documented = [50, 78, 79]
empty_and_boundaries = [
    -100,
    -2,
    -1,
    0,
    1,
    2,
    6,
    7,
    8,
    10,
    11,
    12,
    13,
    14,
    49,
    50,
    51,
    76,
    77,
    78,
    79,
    80,
]
branch_boundaries = [
    # Just before/at/after representative multiples of 11, 13, and 143.
    110,
    111,
    112,
    116,
    117,
    118,
    142,
    143,
    144,
    # Inputs around qualifying numbers containing one or several digit sevens.
    175,
    176,
    177,
    272,
    273,
    274,
    714,
    715,
    716,
    769,
    770,
    771,
    772,
    7776,
    7777,
    7778,
    7779,
]
exhaustive_small = list(range(-25, 513))
random_generator = random.Random(360036)
generated = [random_generator.randint(-500, 10_000) for _ in range(256)]
large = [1_000, 5_000, 10_000, 20_000]

inputs = sorted(
    set(
        documented
        + empty_and_boundaries
        + branch_boundaries
        + exhaustive_small
        + generated
        + large
    )
)
mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        mismatches.append({"n": n, "canonical": expected, "candidate": actual})

selected = {}
for n in [-100, -1, 0, 1, 50, 78, 79, 118, 144, 177, 274, 716, 771, 7778]:
    selected[str(n)] = {
        "canonical": canonical(n),
        "candidate": candidate(n),
    }

print("DOCUMENTED_EXAMPLES:", json.dumps(documented))
print("ALL_TEST_INPUTS:", json.dumps(inputs))
print("INPUT_COUNT:", len(inputs))
print("SELECTED_RESULTS:", json.dumps(selected, sort_keys=True))
print("MISMATCH_COUNT:", len(mismatches))
print("MISMATCHES:", json.dumps(mismatches, sort_keys=True))
raise SystemExit(1 if mismatches else 0)

