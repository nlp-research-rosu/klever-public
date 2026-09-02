#!/usr/bin/env python3
"""Ground witnesses for the entry-claim domains and result formula."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def claimed_result(values: list[int]) -> list[int]:
    """Ground interpretation of condRev(sortVS(input), even(first+last))."""
    if not values:
        return []
    ascending_sort_vs = sorted(values)
    reverse = (values[0] + values[-1]) % 2 == 0
    return list(reversed(ascending_sort_vs)) if reverse else ascending_sort_vs


def main() -> None:
    candidate = load("candidate_witness", ROOT / "solution.py")
    canonical = load("canonical_witness", ROOT / "canonical.py")
    witnesses = [
        [],
        [0, 1],
        [2, 4, 3, 0, 1, 5, 6],
        [10**40 + 1, 0, 10**40],
    ]
    for values in witnesses:
        assert all(isinstance(value, int) and value >= 0 for value in values)
        expected = claimed_result(values)
        generated = candidate.sort_array(list(values))
        trusted = canonical.sort_array(list(values))
        assert generated == trusted == expected
        if values:
            first = values[0]
            tail = values[1:]
            last_index = len(tail)
            last = values[last_index]
            assert last == values[-1]
            print(
                "NONEMPTY_WITNESS "
                f"input={values!r} F={first} IS={tail!r} "
                f"vsLen(IS)={last_index} L={last} result={expected!r}"
            )
        else:
            print("EMPTY_WITNESS input=[] result=[]")
    print("ADEQUACY_WITNESSES PASS")


if __name__ == "__main__":
    main()
