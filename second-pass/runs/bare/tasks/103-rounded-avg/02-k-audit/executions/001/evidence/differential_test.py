#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/103-rounded-avg/candidate-src/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.json")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


def outcome(function, n: int, m: int):
    try:
        value = function(n, m)
        return {"kind": "return", "type": type(value).__name__, "value": repr(value)}
    except Exception as error:  # The exception class is observable behavior here.
        return {"kind": "exception", "type": type(error).__name__, "value": str(error)}


canonical = load_function("trusted_canonical", CANONICAL_PATH)
candidate = load_function("generated_solution", CANDIDATE_PATH)

documented = [(1, 5), (7, 5), (10, 20), (20, 33)]
branch_and_rounding_boundaries = [
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 3),
    (3, 4),
    (3, 5),
    (4, 3),
    (2, 1),
    (100, 99),
]
outside_documented_domain = [(0, 0), (0, 1), (1, 0), (-2, -2), (-1, 2)]

# These cases are short intervals, so the trusted loop remains bounded while
# exercising CPython binary64 conversion boundaries.
large_boundaries = []
for center in (2**52, 2**53, 2**54, 2**1022, 2**1023, 10**400):
    for offset in (-2, -1, 0, 1, 2):
        n = center + offset
        large_boundaries.extend(((n, n), (n, n + 1), (n + 1, n)))

exhaustive_small = [(n, m) for n in range(1, 41) for m in range(1, 41)]
rng = random.Random(103_2026)
generated = [(rng.randint(1, 1_000_000), rng.randint(1, 1_000_000)) for _ in range(1000)]

groups = {
    "documented": documented,
    "branch_and_rounding_boundaries": branch_and_rounding_boundaries,
    "outside_documented_domain": outside_documented_domain,
    "large_binary64_boundaries": large_boundaries,
    "exhaustive_positive_1_through_40": exhaustive_small,
    "seeded_positive_random": generated,
}
INPUT_RECORD.write_text(json.dumps(groups, indent=2) + "\n", encoding="utf-8")
input_hash = hashlib.sha256(INPUT_RECORD.read_bytes()).hexdigest()

expected_examples = {
    (1, 5): {"kind": "return", "type": "str", "value": repr("0b11")},
    (7, 5): {"kind": "return", "type": "int", "value": repr(-1)},
    (10, 20): {"kind": "return", "type": "str", "value": repr("0b1111")},
    (20, 33): {"kind": "return", "type": "str", "value": repr("0b11010")},
}

mismatches = []
example_failures = []
total = 0
for group_name, cases in groups.items():
    for index, (n, m) in enumerate(cases):
        total += 1
        left = outcome(canonical, n, m)
        right = outcome(candidate, n, m)
        if left != right:
            mismatches.append(
                {"group": group_name, "index": index, "n": n, "m": m, "canonical": left, "candidate": right}
            )
        expected = expected_examples.get((n, m))
        if group_name == "documented" and right != expected:
            example_failures.append(
                {"n": n, "m": m, "expected": expected, "candidate": right}
            )

print(f"canonical={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"input_record={INPUT_RECORD}")
print(f"input_record_sha256={input_hash}")
print("groups=" + json.dumps({name: len(cases) for name, cases in groups.items()}, sort_keys=True))
print(f"total_cases={total}")
print(f"mismatch_count={len(mismatches)}")
print(f"documented_example_failure_count={len(example_failures)}")
for mismatch in mismatches[:50]:
    print("MISMATCH " + json.dumps(mismatch, sort_keys=True))
for failure in example_failures:
    print("EXAMPLE_FAILURE " + json.dumps(failure, sort_keys=True))

if mismatches or example_failures:
    sys.exit(1)
