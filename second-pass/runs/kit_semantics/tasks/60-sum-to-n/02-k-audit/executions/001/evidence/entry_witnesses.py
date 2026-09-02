#!/usr/bin/env python3
"""Concrete satisfying witnesses for both entry-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_to_n


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
candidate = load(
    Path("/tmp/audit-work/reconstruction/solution.py"),
    "candidate_witness",
)

witnesses = [
    ("sum-to-n-empty-range", -3, lambda n: 0),
    ("sum-to-n-positive", 5, lambda n: n * (n + 1) // 2),
]
for claim, n, formal_result in witnesses:
    expected = formal_result(n)
    canonical_result = canonical(n)
    candidate_result = candidate(n)
    assert expected == canonical_result == candidate_result
    print(
        f"claim={claim} N={n} formal={expected} "
        f"canonical={canonical_result} candidate={candidate_result}"
    )

print("ENTRY_WITNESSES_PASS")
