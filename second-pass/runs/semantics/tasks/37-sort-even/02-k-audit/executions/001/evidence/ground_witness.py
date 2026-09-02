#!/usr/bin/env python3
"""Evaluate concrete witnesses against both Python bodies and the K post formula."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_sort_even(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def claimed_formula(values):
    evens = sorted(values[::2])
    odds = values[1::2]
    paired = [value for pair in zip(evens, odds) for value in pair]
    suffix = evens[len(odds) :]
    return paired + suffix


def main() -> int:
    root = Path("/tmp/audit-work/37-sort-even-audit")
    canonical = load_sort_even(root / "trusted/canonical.py", "ground_canonical")
    candidate = load_sort_even(root / "source/solution.py", "ground_candidate")
    cases = [[], [7], [5, 6, 3, 4], [9, -1, 3, -2, 3, -3, 0]]
    mismatch_count = 0
    for values in cases:
        formula = claimed_formula(values)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        matches = formula == canonical_result == candidate_result
        mismatch_count += not matches
        print(
            f"input={values!r} claimed_formula={formula!r} "
            f"canonical={canonical_result!r} candidate={candidate_result!r} "
            f"match={matches}"
        )
    print(f"satisfying_entry_states={len(cases)}")
    print(f"mismatches={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
