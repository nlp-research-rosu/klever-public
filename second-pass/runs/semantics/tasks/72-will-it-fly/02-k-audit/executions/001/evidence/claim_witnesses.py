#!/usr/bin/env python3
"""Evaluate one concrete satisfying input for each symbolic entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


def kvals(values: list[int]) -> str:
    term = ".ValSeq"
    for value in reversed(values):
        term = f"vCons({value}, {term})"
    return term


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    generated = load(
        Path("/tmp/audit-work/72-will-it-fly/solution.py"),
        "generated_witness",
    )
    witnesses = [
        ("balanced-within", [3, 2, 3], 9, True),
        ("unbalanced", [1, 2], 5, False),
        ("balanced-overweight", [3, 2, 3], 1, False),
    ]
    for claim, q, w, expected in witnesses:
        record = {
            "claim": claim,
            "q": q,
            "VS": kvals(q),
            "W": w,
            "allInts": all(type(value) is int for value in q),
            "palindrome": q == q[::-1],
            "sum": sum(q),
            "sum_le_W": sum(q) <= w,
            "sum_gt_W": sum(q) > w,
            "canonical": canonical(list(q), w),
            "generated": generated(list(q), w),
            "claimed_result": expected,
        }
        print(json.dumps(record, sort_keys=True))
        assert record["canonical"] == record["generated"] == expected
    print("witness_count=3")
    print("mismatch_count=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
