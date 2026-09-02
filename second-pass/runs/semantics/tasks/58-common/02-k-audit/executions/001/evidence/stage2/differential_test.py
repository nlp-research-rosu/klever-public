#!/usr/bin/env python3
"""Independent differential test for HumanEval 58 `common`.

The oracle and candidate are loaded from separate source files.  Inputs cover
the two documented examples, explicit loop/condition boundaries, an exhaustive
small integer-list product, and deterministic representative random cases.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


ORACLE_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/case58/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/stage2/differential-inputs.json")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


def outcome(function, left, right):
    try:
        return {"kind": "return", "value": function(left.copy(), right.copy())}
    except Exception as error:  # Differentially compare unexpected behavior too.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


documented = [
    ([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]),
    ([5, 3, 2, 8], [3, 2]),
]

# Empty loop/input, false first conjunct, true first + true second conjunct,
# duplicate-suppression false second conjunct, order reversal, negative and
# large integer boundaries.
boundaries = [
    ([], []),
    ([], [1]),
    ([1], []),
    ([1], [1]),
    ([1, 1], [1]),
    ([1, 2], [1]),
    ([2, 1], [1]),
    ([0, -1, 0, 2], [2, 0]),
    ([-10**100, 10**100, -10**100], [10**100, -10**100]),
]

alphabet = (-2, -1, 0, 1, 2)
small_lists = [
    list(values)
    for length in range(4)
    for values in itertools.product(alphabet, repeat=length)
]
exhaustive = [(left, right) for left in small_lists for right in small_lists]

rng = random.Random(580058)
random_cases = []
for _ in range(1000):
    left = [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 20))]
    right = [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 20))]
    random_cases.append((left, right))

cases = documented + boundaries + exhaustive + random_cases
INPUTS_PATH.write_text(
    json.dumps(
        {
            "documented_count": len(documented),
            "boundary_count": len(boundaries),
            "exhaustive_description": (
                "all ordered pairs of lists of length 0..3 "
                "over integer alphabet [-2,-1,0,1,2]"
            ),
            "exhaustive_count": len(exhaustive),
            "random_seed": 580058,
            "random_description": (
                "1000 pairs, each length 0..20, integer values -1000..1000"
            ),
            "random_count": len(random_cases),
            "cases": cases,
        },
        separators=(",", ":"),
    )
    + "\n",
    encoding="utf-8",
)

oracle = load_entry("trusted_canonical_58", ORACLE_PATH)
candidate = load_entry("scratch_candidate_58", CANDIDATE_PATH)

mismatches = []
for index, (left, right) in enumerate(cases):
    expected = outcome(oracle, left, right)
    actual = outcome(candidate, left, right)
    if expected != actual:
        mismatches.append(
            {
                "index": index,
                "left": left,
                "right": right,
                "oracle": expected,
                "candidate": actual,
            }
        )
        if len(mismatches) >= 20:
            break

print(f"oracle={ORACLE_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"documented={len(documented)}")
print(f"boundaries={len(boundaries)}")
print(f"exhaustive={len(exhaustive)}")
print(f"random={len(random_cases)} seed=580058")
print(f"total={len(cases)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2, sort_keys=True))
    raise SystemExit(1)
