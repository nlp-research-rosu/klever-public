#!/usr/bin/env python3
"""Substitute concrete strings into the claim's sameSet(dedupCodes(...)) result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/54-same-chars")


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.same_chars


def dedup_codes(codes: list[int]) -> list[int]:
    accumulator: list[int] = []
    for code in codes:
        if code not in accumulator:
            accumulator.append(code)
    return accumulator


def subset_codes(left: list[int], right: list[int]) -> bool:
    return all(code in right for code in left)


def claimed_result(left: str, right: str) -> bool:
    left_codes = dedup_codes([ord(char) for char in left])
    right_codes = dedup_codes([ord(char) for char in right])
    return subset_codes(left_codes, right_codes) and subset_codes(
        right_codes, left_codes
    )


candidate = load_entry("ground_candidate", SCRATCH / "solution.py")
canonical = load_entry("ground_canonical", SCRATCH / "canonical.py")
cases = [
    ("", ""),
    ("", "a"),
    ("a", "aa"),
    ("a", "b"),
    ("ab", "bbaa"),
    ("abc", "ab"),
]

failures = 0
for left, right in cases:
    formula = claimed_result(left, right)
    candidate_value = candidate(left, right)
    canonical_value = canonical(left, right)
    print(
        f"left={left!r} right={right!r} "
        f"S0={[ord(c) for c in left]!r} S1={[ord(c) for c in right]!r} "
        f"dedup0={dedup_codes([ord(c) for c in left])!r} "
        f"dedup1={dedup_codes([ord(c) for c in right])!r} "
        f"sameSet={formula} candidate={candidate_value} canonical={canonical_value}"
    )
    if not (formula == candidate_value == canonical_value):
        failures += 1
print(f"cases={len(cases)} failures={failures}")
if failures:
    raise SystemExit(1)
