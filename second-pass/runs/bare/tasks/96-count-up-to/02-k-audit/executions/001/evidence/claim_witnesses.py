#!/usr/bin/env python3
"""Concrete satisfying witnesses for all three submitted claim preconditions."""

from __future__ import annotations

import importlib.util
import json
import pathlib
from types import ModuleType


def load_module(name: str, path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def no_factor(c: int, d: int) -> bool:
    while d * d <= c:
        if c % d == 0:
            return False
        d += 1
    return True


def primes_from(c: int, n: int) -> list[int]:
    return [value for value in range(c, n) if value >= 2 and no_factor(value, 2)]


def main() -> int:
    canonical = load_module("trusted_canonical_witness", pathlib.Path("/reference/canonical.py"))
    submitted = load_module(
        "submitted_solution_witness",
        pathlib.Path("/tmp/audit-work/96-count-up-to/solution.py"),
    )

    trial = {"C": 4, "D": 2, "B": True, "N": 5, "K": ".K"}
    scan = {"C": 2, "N": 5, "K": ".K"}
    entry = {"N": 5, "result_initial": ".K"}
    print("trial_precondition_witness=" + json.dumps(trial, sort_keys=True))
    print(f"trial_precondition_holds={trial['C'] >= 2 and trial['D'] >= 2}")
    print(f"noFactor(4,2)={no_factor(4, 2)}")
    print("trial_claimed_boolean=True and noFactor(4,2)=False")
    print("trial_concrete_successor=scan(5,5) ~> prependIf(4,false) ~> .K")

    print("scan_precondition_witness=" + json.dumps(scan, sort_keys=True))
    print(f"scan_precondition_holds={scan['C'] >= 2}")
    print(f"primesFrom(2,5)={primes_from(2, 5)}")

    print("entry_precondition_witness=" + json.dumps(entry, sort_keys=True))
    print(f"entry_precondition_holds={entry['N'] >= 0}")
    print(f"claimed_primesBelow(5)={primes_from(2, 5)}")
    print(f"canonical_count_up_to(5)={canonical.count_up_to(5)}")
    print(f"submitted_count_up_to(5)={submitted.count_up_to(5)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
