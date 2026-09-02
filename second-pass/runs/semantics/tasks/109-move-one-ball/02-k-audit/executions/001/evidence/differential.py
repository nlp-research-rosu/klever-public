#!/usr/bin/env python3
"""Independent differential audit for HumanEval 109.

Oracle: /reference/canonical.py (trusted canonical implementation).
Subject: scratch copy of the submitted /candidate/solution.py.

The intended domain is finite Python lists of pairwise-distinct integers.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
SUBJECT_PATH = Path("/tmp/audit-work/109-move-one-ball/candidate/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.jsonl")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_109", CANONICAL_PATH).move_one_ball
subject = load("candidate_solution_109", SUBJECT_PATH).move_one_ball

documented_and_branch_cases = [
    ("documented-true", [3, 4, 5, 1, 2]),
    ("documented-false", [3, 5, 4, 1, 2]),
    ("empty-return", []),
    ("singleton-zero-drops", [7]),
    ("two-ascending-wrap-drop-only", [1, 2]),
    ("two-descending-loop-drop-only", [2, 1]),
    ("one-loop-drop-no-wrap-drop", [3, 1, 2]),
    ("no-loop-drop-one-wrap-drop", [-5, 0, 8]),
    ("one-loop-plus-one-wrap-two-drops", [1, 3, 2]),
    ("two-loop-drops-no-wrap-drop", [3, 2, 1]),
    ("large-integers-accepted", [10**40, -10**40, 0]),
    ("large-integers-rejected", [-10**40, 10**40, 0]),
]

all_cases: list[tuple[str, list[int]]] = list(documented_and_branch_cases)

# Every ordering of a fixed pairwise-distinct integer set for lengths 0..8.
for n in range(9):
    values = tuple(range(-n // 2, -n // 2 + n))
    for perm in itertools.permutations(values):
        all_cases.append((f"exhaustive-permutation-n{n}", list(perm)))

# Deterministic representative samples with wider lengths and values.
rng = random.Random(109_2026)
for _ in range(5_000):
    n = rng.randrange(0, 33)
    values = rng.sample(range(-10_000, 10_001), n)
    rng.shuffle(values)
    all_cases.append(("seeded-random-unique", values))

# Supplemental out-of-contract duplicate cases probe the broader K claim.
for case in (
    [],
    [0],
    [1, 1],
    [1, 2, 1],
    [2, 1, 1],
    [1, 2, 2, 1],
    [2, 2, 1, 1],
    [3, 1, 2, 2],
):
    all_cases.append(("supplemental-duplicates", case))

intended_mismatches: list[dict[str, object]] = []
supplemental_mismatches: list[dict[str, object]] = []
serialized = []
for index, (label, arr) in enumerate(all_cases):
    expected = canonical(list(arr))
    actual = subject(list(arr))
    record = {
        "index": index,
        "label": label,
        "input": arr,
        "canonical": expected,
        "candidate": actual,
    }
    line = json.dumps(record, sort_keys=True, separators=(",", ":"))
    serialized.append(line)
    if type(expected) is not type(actual) or expected != actual:
        if label == "supplemental-duplicates":
            supplemental_mismatches.append(record)
        else:
            intended_mismatches.append(record)

payload = ("\n".join(serialized) + "\n").encode()
INPUTS_PATH.write_bytes(payload)

print(f"canonical={CANONICAL_PATH}")
print(f"subject={SUBJECT_PATH}")
print(f"inputs_file={INPUTS_PATH}")
print(f"inputs_sha256={hashlib.sha256(payload).hexdigest()}")
print(f"documented_and_branch_cases={len(documented_and_branch_cases)}")
print("exhaustive_permutation_lengths=0..8")
print("seeded_random_unique_count=5000 seed=1092026 length=0..32")
print("supplemental_duplicate_count=8")
print(f"total_cases={len(all_cases)}")
print(f"intended_domain_mismatches={len(intended_mismatches)}")
print(f"supplemental_out_of_contract_mismatches={len(supplemental_mismatches)}")
for record in intended_mismatches[:20]:
    print("INTENDED_MISMATCH " + json.dumps(record, sort_keys=True))
for record in supplemental_mismatches[:20]:
    print("OUT_OF_CONTRACT_MISMATCH " + json.dumps(record, sort_keys=True))

sys.exit(1 if intended_mismatches else 0)
