#!/usr/bin/env python3
"""Ground witnesses and substitutions for every candidate entry input."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXPECTED = {
    1: [],
    2: [2],
    3: [3],
    4: [2, 2],
    8: [2, 2, 2],
    9: [3, 3],
    13: [13],
    25: [5, 5],
    31: [31],
    70: [2, 5, 7],
    100: [2, 2, 5, 5],
    360: [2, 2, 2, 3, 3, 5],
    999: [3, 3, 3, 37],
}


def main() -> None:
    canonical = load_module("claim_canonical", Path("/reference/canonical.py"))
    candidate = load_module(
        "claim_candidate", Path("/tmp/audit-work/25-factorize/solution.py")
    )
    print(
        "Each exact claim has the ground satisfying source "
        "Run(SolutionMachine(n)); each contract claim has the ground "
        "satisfying source Observe(ValidFactorization(n, "
        "MachineValue(SolutionMachine(n))))."
    )
    for index, (value, expected) in enumerate(EXPECTED.items(), 1):
        canonical_result = canonical.factorize(value)
        candidate_result = candidate.factorize(value)
        exact_ok = canonical_result == candidate_result == expected
        print(
            f"claims {index:02d}/{index + 13:02d}: n={value} "
            f"post={expected} canonical={canonical_result} "
            f"candidate={candidate_result} substitution_match={exact_ok}"
        )
        if not exact_ok:
            raise AssertionError(f"claim witness mismatch at n={value}")
    print("CLAIM_WITNESS_SUBSTITUTIONS=PASS count=26")


if __name__ == "__main__":
    main()
