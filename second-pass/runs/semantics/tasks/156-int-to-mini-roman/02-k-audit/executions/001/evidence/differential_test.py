#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval 156."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate/solution.py")
canonical = load(CANONICAL_PATH, "trusted_canonical")
candidate = load(CANDIDATE_PATH, "generated_candidate")

examples = {19: "xix", 152: "clii", 426: "cdxxvi"}
branch_landmarks = [
    1,
    3,
    4,
    5,
    8,
    9,
    10,
    39,
    40,
    41,
    49,
    50,
    51,
    89,
    90,
    91,
    99,
    100,
    101,
    399,
    400,
    401,
    499,
    500,
    501,
    899,
    900,
    901,
    944,
    999,
    1000,
]

failures: list[str] = []
rows: list[tuple[int, str, str]] = []

# The integer contract has no container-like empty input. Zero is checked as
# the natural empty-result edge immediately below the stated positive domain.
zero_canonical = canonical.int_to_mini_roman(0)
zero_candidate = candidate.int_to_mini_roman(0)
if zero_canonical != zero_candidate:
    failures.append(
        f"outside-domain zero edge differs: canonical={zero_canonical!r}, "
        f"candidate={zero_candidate!r}"
    )

for number in range(1, 1001):
    expected = canonical.int_to_mini_roman(number)
    actual = candidate.int_to_mini_roman(number)
    rows.append((number, expected, actual))
    if actual != expected:
        failures.append(f"N={number}: canonical={expected!r}, candidate={actual!r}")
    if not isinstance(actual, str) or actual != actual.lower():
        failures.append(f"N={number}: result is not a lowercase string: {actual!r}")

for number, expected in examples.items():
    actual = candidate.int_to_mini_roman(number)
    if actual != expected:
        failures.append(f"documented example N={number}: expected={expected!r}, got={actual!r}")

result_digest = hashlib.sha256(
    json.dumps(rows, separators=(",", ":")).encode("utf-8")
).hexdigest()
print(f"canonical={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print("contract_domain=all integers 1..1000 inclusive")
print(f"documented_examples={examples}")
print(f"branch_and_boundary_landmarks={branch_landmarks}")
print(f"zero_empty_result_edge=canonical:{zero_canonical!r},candidate:{zero_candidate!r}")
print(f"tested_domain_count={len(rows)}")
print(f"complete_result_table_sha256={result_digest}")
print(f"mismatch_count={len(failures)}")
for failure in failures[:50]:
    print(f"MISMATCH {failure}")

if failures:
    raise SystemExit(1)
