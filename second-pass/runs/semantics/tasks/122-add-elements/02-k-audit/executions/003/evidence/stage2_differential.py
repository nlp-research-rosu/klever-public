#!/usr/bin/env python3
"""Deterministic differential audit of canonical.py versus solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/122-add-elements-audit")
INPUT_RECORD = Path("/audit-output/evidence/stage2-differential-inputs.json")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add_elements


def main() -> int:
    canonical = load_entry("trusted_canonical", WORK / "canonical.py")
    candidate = load_entry("generated_candidate", WORK / "solution.py")

    cases: list[dict[str, object]] = [
        {
            "label": "documented-example",
            "arr": [111, 21, 3, 4000, 5, 6, 7, 8, 9],
            "k": 4,
        },
        {"label": "minimum-length-zero", "arr": [0], "k": 1},
        {"label": "minimum-length-positive", "arr": [9], "k": 1},
        {"label": "minimum-length-negative-one-digit", "arr": [-9], "k": 1},
        {"label": "negative-two-digit-boundary", "arr": [-99], "k": 1},
        {
            "label": "all-value-branch-boundaries",
            "arr": [-1000, -100, -99, -10, -9, -1, 0, 9, 10, 99, 100, 1000],
            "k": 12,
        },
        {
            "label": "k-lower-bound",
            "arr": [-99, 5, 100],
            "k": 1,
        },
        {
            "label": "k-upper-bound",
            "arr": [-99, 5, 100],
            "k": 3,
        },
        {
            "label": "maximum-length",
            "arr": ([-99, -9, 0, 99, 100] * 20),
            "k": 100,
        },
    ]

    seed = 12220260726
    rng = random.Random(seed)
    boundary_pool = [
        -10000,
        -1000,
        -101,
        -100,
        -99,
        -98,
        -11,
        -10,
        -9,
        -1,
        0,
        1,
        9,
        10,
        11,
        98,
        99,
        100,
        101,
        1000,
        10000,
    ]
    for index in range(5000):
        length = rng.randint(1, 100)
        arr = [
            (
                boundary_pool[rng.randrange(len(boundary_pool))]
                if rng.random() < 0.55
                else rng.randint(-100000, 100000)
            )
            for _ in range(length)
        ]
        k = rng.randint(1, length)
        cases.append(
            {
                "label": f"generated-{index:04d}",
                "arr": arr,
                "k": k,
            }
        )

    input_document = {
        "contract_domain": {
            "arr": "list[int], 1 <= len(arr) <= 100",
            "k": "int, 1 <= k <= len(arr)",
        },
        "seed": seed,
        "boundary_pool": boundary_pool,
        "cases": cases,
        "outside_contract_diagnostics": [
            {"label": "empty-arr-k-zero", "arr": [], "k": 0},
        ],
    }
    encoded = (
        json.dumps(input_document, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    )
    INPUT_RECORD.write_bytes(encoded)
    print(f"input_record={INPUT_RECORD}")
    print(f"input_record_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"intended_domain_case_count={len(cases)}")
    print(f"seed={seed}")
    print(f"boundary_pool={boundary_pool}")

    mismatches = []
    for case in cases:
        arr = case["arr"]
        k = case["k"]
        expected = canonical(arr, k)
        actual = candidate(arr, k)
        if actual != expected:
            mismatches.append(
                {
                    "label": case["label"],
                    "arr": arr,
                    "k": k,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    outside = input_document["outside_contract_diagnostics"][0]
    outside_expected = canonical(outside["arr"], outside["k"])
    outside_actual = candidate(outside["arr"], outside["k"])
    print(
        "outside_contract "
        f"label={outside['label']} canonical={outside_expected} "
        f"candidate={outside_actual}"
    )

    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:30]:
        print("MISMATCH " + json.dumps(mismatch, sort_keys=True))
    if len(mismatches) > 30:
        print(f"MISMATCH_OUTPUT_TRUNCATED remaining={len(mismatches) - 30}")

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
