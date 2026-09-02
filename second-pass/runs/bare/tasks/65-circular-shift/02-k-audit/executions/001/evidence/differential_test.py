#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval 65."""

import importlib.util
import json
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

# The source contract accepts integer x and integer shift.  No integer has an
# empty decimal rendering, so x=0 and one-character renderings are the closest
# valid boundary cases.  Negative shifts are included because the prompt gives
# no nonnegative precondition.
documented = [(12, 1), (12, 2)]
fixed_x = [0, 1, -1, 9, -9, 10, -10, 12, -12, 100, -100, 1234, -1234]
cases = list(documented)
for x in fixed_x:
    width = len(str(x))
    for shift in [-width - 2, -1, 0, 1, max(0, width - 1), width, width + 1, width + 2]:
        cases.append((x, shift))

rng = random.Random(650065)
for _ in range(64):
    x = rng.randint(-(10**30), 10**30)
    width = len(str(x))
    shift = rng.randint(-2 * width - 3, 2 * width + 3)
    cases.append((x, shift))

# Deduplicate without changing order so the exact logged input set is stable.
cases = list(dict.fromkeys(cases))
mismatches = []
for index, (x, shift) in enumerate(cases):
    expected = canonical(x, shift)
    actual = candidate(x, shift)
    record = {
        "index": index,
        "x": x,
        "shift": shift,
        "canonical": expected,
        "candidate": actual,
        "match": expected == actual,
    }
    print(json.dumps(record, sort_keys=True))
    if expected != actual:
        mismatches.append(record)

print(
    json.dumps(
        {
            "summary": {
                "case_count": len(cases),
                "mismatch_count": len(mismatches),
                "documented_examples": documented,
                "random_seed": 650065,
            }
        },
        sort_keys=True,
    )
)
sys.exit(1 if mismatches else 0)
