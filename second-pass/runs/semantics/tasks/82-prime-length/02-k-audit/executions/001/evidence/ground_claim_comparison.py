#!/usr/bin/env python3
"""Concrete substitutions into each submitted claim's RHS."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def no_divisors_from(n: int, d: int) -> bool:
    if d >= n:
        return True
    if n % d == 0:
        return False
    return no_divisors_from(n, d + 1)


canonical = load_module("canonical_ground", Path("/reference/canonical.py"))
candidate = load_module("candidate_ground", Path("/tmp/audit-work/82/solution.py"))

for text in ("", "a"):
    print(
        "prime-length-small",
        repr(text),
        f"pre=len({len(text)})<2",
        "claimed-RHS=False",
        f"canonical={canonical.prime_length(text)!r}",
        f"candidate={candidate.prime_length(text)!r}",
    )

for text in ("ab", "abcde", "abcd"):
    print(
        "prime-length-setup",
        repr(text),
        f"pre=len({len(text)})>=2",
        f"claimed-RHS=#primeLoopEntry({len(text)},2)",
        f"canonical={canonical.prime_length(text)!r}",
        f"candidate={candidate.prime_length(text)!r}",
        "RHS_IS_NOT_A_BOOLEAN",
    )

for n, d in ((5, 2), (4, 2), (2, 2), (9, 2)):
    summary = no_divisors_from(n, d)
    witness = "x" * n
    print(
        "divisor-loop",
        f"N={n}",
        f"D={d}",
        f"claimed-RHS=noDivisorsFrom({n},{d})={summary!r}",
        f"canonical-entry={canonical.prime_length(witness)!r}",
        f"candidate-entry={candidate.prime_length(witness)!r}",
        "ENTRY_COMPARISON_ONLY_VALID_WHEN_D=2",
    )
