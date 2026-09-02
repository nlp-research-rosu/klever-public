#!/usr/bin/env python3
"""Independent differential test of canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
candidate = load_entry("/tmp/audit-work/candidate/solution.py", "generated_solution")

# Examples, positivity boundary, threshold branch boundaries, reversed endpoints,
# equal endpoints, intervals wholly outside the digit range, and broad integers.
fixed = [
    (2, 8),
    (8, 2),
    (10, 14),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 3),
    (3, 4),
    (4, 3),
    (4, 4),
    (5, 5),
    (5, 6),
    (6, 5),
    (6, 6),
    (7, 7),
    (7, 8),
    (8, 7),
    (8, 8),
    (8, 9),
    (9, 8),
    (9, 9),
    (1, 9),
    (9, 1),
    (3, 7),
    (7, 3),
    (1, 10),
    (10, 1),
    (100, 101),
    (101, 100),
    (1, 10**30),
    (10**30, 1),
]

# Exhaust all small positive pairs spanning every comparison boundary.
cases = fixed + [(a, b) for a in range(1, 18) for b in range(1, 18)]
random.seed(163)
cases += [(random.randint(1, 10**9), random.randint(1, 10**9)) for _ in range(500)]

mismatches = []
records = []
for a, b in cases:
    expected = canonical(a, b)
    actual = candidate(a, b)
    if expected != actual:
        mismatches.append({"input": [a, b], "canonical": expected, "candidate": actual})
    if (a, b) in fixed:
        records.append({"input": [a, b], "canonical": expected, "candidate": actual})

print(json.dumps({"fixed_results": records}, indent=2, sort_keys=True))
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps({"mismatches": mismatches[:20]}, indent=2, sort_keys=True))
    raise SystemExit(1)
print("DIFFERENTIAL_TEST=PASS")
