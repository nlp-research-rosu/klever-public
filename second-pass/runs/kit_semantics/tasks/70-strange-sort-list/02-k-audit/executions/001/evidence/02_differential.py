#!/usr/bin/env python3
"""Independent return-value differential for HumanEval/70.

Oracle 1 is the trusted canonical entry point. Oracle 2 is a locally written
specification function that repeatedly selects the low/high endpoints of a
sorted copy. The candidate is imported from the fresh scratch reconstruction.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction.tZYoqF/solution.py")
EXHAUSTIVE_VALUES = (-2, -1, 0, 2)
EXHAUSTIVE_MAX_LENGTH = 8
RANDOM_SEED = 700070
RANDOM_CASES = 2000


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strange_sort_list


canonical = load_entry(CANONICAL_PATH, "trusted_humaneval_70_canonical")
candidate = load_entry(CANDIDATE_PATH, "scratch_humaneval_70_candidate")


def independent_oracle(values: list[int]) -> list[int]:
    ordered = sorted(values)
    result: list[int] = []
    low = 0
    high = len(ordered) - 1
    while low <= high:
        result.append(ordered[low])
        low += 1
        if low <= high:
            result.append(ordered[high])
            high -= 1
    return result


named_cases = [
    ("documented-length-4", [1, 2, 3, 4]),
    ("documented-duplicates", [5, 5, 5, 5]),
    ("documented-empty", []),
    ("singleton-if-true", [9]),
    ("length-2-loop-once-if-false", [2, 1]),
    ("length-3-loop-once-if-true", [3, 1, 2]),
    ("length-4-loop-twice-if-false", [4, 1, 3, 2]),
    ("length-5-loop-twice-if-true", [4, -1, 3, 2, 0]),
    ("negative-duplicates", [-3, -1, -3, -2, -1]),
    ("large-magnitude", [-(10**100), 10**100, 0, -1, 1]),
]

mismatches: list[tuple[str, list[int], list[int], list[int], list[int]]] = []
checked = 0


def check(label: str, values: list[int], *, display: bool = False) -> None:
    global checked
    expected = independent_oracle(values)
    canonical_arg = list(values)
    candidate_arg = list(values)
    canonical_result = canonical(canonical_arg)
    candidate_result = candidate(candidate_arg)
    checked += 1
    if display:
        print(
            f"{label}: input={values!r} expected={expected!r} "
            f"canonical={canonical_result!r} candidate={candidate_result!r}"
        )
    if canonical_result != expected or candidate_result != expected:
        mismatches.append(
            (label, values, expected, canonical_result, candidate_result)
        )


print(f"canonical_path={CANONICAL_PATH}")
print(f"candidate_path={CANDIDATE_PATH}")
for case_label, case_values in named_cases:
    check(case_label, case_values, display=True)

for length in range(EXHAUSTIVE_MAX_LENGTH + 1):
    for values in itertools.product(EXHAUSTIVE_VALUES, repeat=length):
        check(f"exhaustive-length-{length}", list(values))

rng = random.Random(RANDOM_SEED)
for index in range(RANDOM_CASES):
    length = rng.randrange(0, 41)
    values = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
    check(f"random-{index}", values)

print(
    "exhaustive_scope="
    f"values={EXHAUSTIVE_VALUES}, lengths=0..{EXHAUSTIVE_MAX_LENGTH}"
)
print(
    f"random_scope=seed={RANDOM_SEED}, cases={RANDOM_CASES}, "
    "lengths=0..40, values=[-10^12,10^12]"
)
print(f"checked={checked}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}", file=sys.stderr)
    raise SystemExit(1)
