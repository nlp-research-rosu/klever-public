#!/usr/bin/env python3
"""Ground witnesses for the entry and auxiliary claim postconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prefix_below(balance: int, remaining: list[int]) -> bool:
    for operation in remaining:
        balance += operation
        if balance < 0:
            return True
    return False


def main() -> int:
    canonical = load(
        "adequacy_canonical",
        Path("/tmp/audit-work/rebuild/trusted/canonical.py"),
    )
    generated = load(
        "adequacy_generated",
        Path("/tmp/audit-work/rebuild/candidate/solution.py"),
    )
    cases = [
        ("main_empty", 0, [], []),
        ("main_documented_true", 0, [1, 2, -4, 5], [1, 2, -4, 5]),
        # A reachable AUX loop-head after consuming the first operation 5.
        ("aux_exact_zero", 5, [-5], [5, -5]),
        # A reachable AUX loop-head at function entry with early return.
        ("aux_early_true", 0, [-1, 100], [-1, 100]),
    ]
    failures = 0
    for name, balance, remaining, full_input in cases:
        claimed = prefix_below(balance, remaining)
        expected = canonical.below_zero(list(full_input))
        actual = generated.below_zero(list(full_input))
        ok = claimed == expected == actual
        failures += not ok
        print(
            f"{name}: B={balance} remaining={remaining} full_input={full_input} "
            f"prefixBelow={claimed} canonical={expected} generated={actual} ok={ok}"
        )
    print(
        "AUX satisfying state: B=5, IS=intCons(-5,.IntVals), "
        "INPUT=intCons(5,intCons(-5,.IntVals)), OLD=5, MODULE=.Map, "
        "BUILTINS=builtinsScope, HEAP=.Map, NEXT=0; fixed cells as in AUX-SPEC."
    )
    print(
        "MAIN satisfying state: IS=intCons(1,intCons(2,intCons(-4,"
        "intCons(5,.IntVals)))); initial cells exactly as in MAIN-SPEC."
    )
    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
