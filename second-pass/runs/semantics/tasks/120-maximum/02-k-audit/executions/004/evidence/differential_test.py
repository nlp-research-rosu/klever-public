#!/usr/bin/env python3
"""Independent result differential for HumanEval 120.

The tested inputs are serialized to differential-inputs.jsonl so the exact
corpus is retained.  The oracle is defined independently of both imported
implementations.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/maximum-120-audit")
EVIDENCE = Path("/audit-output/evidence")
SEED = 120_20260726


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.maximum


canonical = load_entry(ROOT / "canonical.py", "trusted_canonical_120")
generated = load_entry(ROOT / "solution.py", "candidate_generated_120")


def oracle(arr: list[int], k: int) -> list[int]:
    ascending = sorted(arr)
    if k == 0:
        return []
    return ascending[len(ascending) - k :]


cases: list[tuple[str, list[int], int]] = [
    ("example", [-3, -4, 5], 3),
    ("example", [4, -4, 4], 2),
    ("example", [-3, 2, 1, 2, -1, -2, 1], 1),
    # Required audit probe outside the source-domain minimum length.
    ("empty-extension", [], 0),
    ("boundary", [-1000], 0),
    ("boundary", [-1000], 1),
    ("boundary", [1000], 0),
    ("boundary", [1000], 1),
    ("boundary", [-1000, 1000], 0),
    ("boundary", [-1000, 1000], 1),
    ("boundary", [-1000, 1000], 2),
    ("boundary", [7, 7, 7, 7], 1),
    ("boundary", [7, 7, 7, 7], 3),
    ("boundary", [7, 7, 7, 7], 4),
]

# Exhaust all arrays through length 4 over representative/boundary values and
# all legal k.  This covers both sides of k == 0 and k == len(arr).
alphabet = (-1000, -1, 0, 1, 1000)
for n in range(1, 5):
    for values in itertools.product(alphabet, repeat=n):
        for k in range(n + 1):
            cases.append(("exhaustive-small", list(values), k))

rng = random.Random(SEED)
for _ in range(250):
    n = rng.randint(1, 1000)
    arr = [rng.randint(-1000, 1000) for _ in range(n)]
    ks = {0, 1, n // 2, max(0, n - 1), n}
    for k in sorted(ks):
        cases.append(("generated", arr, k))

# Explicit maximum-length/element-bound cases.
cases.extend(
    [
        ("max-length", [-1000] * 1000, 1000),
        ("max-length", [1000] * 1000, 999),
        ("max-length", list(range(-500, 500)), 500),
    ]
)

mismatches: list[dict[str, object]] = []
category_counts: dict[str, int] = {}
with (EVIDENCE / "differential-inputs.jsonl").open("w", encoding="utf-8") as out:
    for index, (category, arr, k) in enumerate(cases):
        record = {"index": index, "category": category, "arr": arr, "k": k}
        out.write(json.dumps(record, separators=(",", ":")) + "\n")
        category_counts[category] = category_counts.get(category, 0) + 1

        expected = oracle(arr, k)
        canonical_input = arr.copy()
        generated_input = arr.copy()
        canonical_result = canonical(canonical_input, k)
        generated_result = generated(generated_input, k)
        if canonical_result != expected or generated_result != expected:
            mismatches.append(
                {
                    **record,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "generated": generated_result,
                }
            )

print(f"seed={SEED}")
print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:10], sort_keys=True))
    raise SystemExit(1)
