#!/usr/bin/env python3
"""Independent integer-domain differential test for HumanEval/52."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_module(
        "candidate_generated", Path("/tmp/audit-work/rebuild-52/solution.py")
    )

    named_cases: list[tuple[str, list[int], int]] = [
        ("prompt-true", [1, 2, 4, 10], 100),
        ("prompt-false", [1, 20, 4, 10], 5),
        ("empty-negative-threshold", [], -100),
        ("empty-zero-threshold", [], 0),
        ("empty-positive-threshold", [], 100),
        ("equal-singleton", [5], 5),
        ("one-below-singleton", [4], 5),
        ("one-above-singleton", [6], 5),
        ("first-element-fails", [0, -2, -3], 0),
        ("middle-element-fails", [-2, 0, -3], 0),
        ("last-element-fails", [-2, -3, 0], 0),
        ("all-negative-pass", [-10, -9, -8], -7),
        ("large-int-pass", [-(10**100), 10**100 - 1], 10**100),
        ("large-int-fail", [10**100], 10**100),
    ]

    cases: list[tuple[str, list[int], int]] = list(named_cases)
    values = range(-3, 4)
    for length in range(5):
        for items in itertools.product(values, repeat=length):
            for threshold in values:
                cases.append(("exhaustive-small", list(items), threshold))

    rng = random.Random(520052)
    for _ in range(2_000):
        length = rng.randrange(0, 31)
        items = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
        threshold = rng.randrange(-(10**12), 10**12 + 1)
        cases.append(("seeded-random", items, threshold))

    digest = hashlib.sha256()
    mismatches: list[dict[str, object]] = []
    for label, items, threshold in cases:
        expected_math = all(item < threshold for item in items)
        expected_canonical = canonical.below_threshold(list(items), threshold)
        actual = generated.below_threshold(list(items), threshold)
        record = {
            "label": label,
            "items": items,
            "threshold": threshold,
            "math": expected_math,
            "canonical": expected_canonical,
            "candidate": actual,
        }
        digest.update(
            (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()
        )
        if not (actual is expected_canonical is expected_math):
            mismatches.append(record)

    print("oracle: trusted canonical plus independent all(x < t for x in l)")
    print("documented/named cases:", len(named_cases))
    print("exhaustive domain: lengths 0..4, elements -3..3, thresholds -3..3")
    print("seeded random domain: 2000 lists, lengths 0..30, seed 520052")
    print("total comparisons:", len(cases))
    print("input/result stream sha256:", digest.hexdigest())
    print("mismatches:", len(mismatches))
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, sort_keys=True))
    assert not mismatches
    print("DIFFERENTIAL_TEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
