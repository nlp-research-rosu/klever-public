#!/usr/bin/env python3
"""Concrete satisfying preconditions and independent expected results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/prime-length-audit")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def no_divisors_from(n: int, divisor: int) -> bool:
    while divisor < n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


canonical = load("ground_canonical", ROOT / "canonical.py")
candidate = load("ground_candidate", ROOT / "solution.py")

entry_witnesses = [
    ("prime-length-small", "", "CS=.IntSeq; isLen(CS)=0"),
    (
        "prime-length-setup",
        "ab",
        "CS=iCons(97,iCons(98,.IntSeq)); isLen(CS)=2",
    ),
]
print("entry_precondition_witnesses:")
for claim, value, formal in entry_witnesses:
    print(
        f"  claim={claim} formal={formal} value={value!r} "
        f"canonical={canonical.prime_length(value)} "
        f"candidate={candidate.prime_length(value)}"
    )

loop_witnesses = [(2, 2), (4, 2), (5, 2), (9, 2), (11, 2), (11, 5)]
print("loop_precondition_witnesses:")
for n, divisor in loop_witnesses:
    string_value = "a" * n
    print(
        f"  N={n} D={divisor} D>=2={divisor >= 2} "
        f"noDivisorsFrom={no_divisors_from(n, divisor)} "
        f"canonical_entry={canonical.prime_length(string_value)} "
        f"candidate_entry={candidate.prime_length(string_value)}"
    )
