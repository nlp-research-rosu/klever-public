#!/usr/bin/env python3
"""Probe the trusted canonical's Python-float precision boundary."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


def first_difference(left: list[int], right: list[int]):
    for index, (l_item, r_item) in enumerate(zip(left, right)):
        if l_item != r_item:
            return index, l_item, r_item
    if len(left) != len(right):
        return min(len(left), len(right)), None, None
    return None


def mathematical_prompt_oracle(n: int) -> list[int]:
    """Literal unbounded-integer recurrence from prompt.py."""
    sequence = [n]
    while sequence[-1] != 1:
        current = sequence[-1]
        sequence.append(current // 2 if current % 2 == 0 else 3 * current + 1)
    return sorted(item for item in sequence if item % 2 == 1)


canonical = load_entry(
    "trusted_canonical_precision", Path("/tmp/audit-work/reference/canonical.py")
)
candidate = load_entry(
    "candidate_solution_precision", Path("/tmp/audit-work/candidate-src/solution.py")
)

inputs = [2**53 - 1, 2**53 + 1, 2**53 + 3, 2**53 + 7, 2**54 + 3]
mismatch_count = 0
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    mathematical = mathematical_prompt_oracle(n)
    differs = expected != actual
    mismatch_count += int(differs)
    print(
        f"n={n} equal={not differs} canonical_len={len(expected)} "
        f"candidate_len={len(actual)} first_difference={first_difference(expected, actual)!r} "
        f"candidate_matches_prompt_oracle={actual == mathematical}"
    )
    if differs:
        print(f"  canonical_head={expected[:12]!r}")
        print(f"  candidate_head={actual[:12]!r}")

print(f"precision_boundary_mismatch_count={mismatch_count}")
raise SystemExit(1 if mismatch_count else 0)
