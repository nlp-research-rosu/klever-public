#!/usr/bin/env python3
"""Exhibit satisfying entry states and concrete postcondition substitutions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/159-eat-audit")


def import_from(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = import_from(ROOT / "trusted/canonical.py", "witness_canonical")
solution = import_from(ROOT / "rebuild/solution.py", "witness_solution")

witnesses = [
    ("symbolic-enough", (5, 6, 10), [11, 4]),
    ("symbolic-insufficient", (2, 11, 5), [7, 0]),
    ("example-1", (5, 6, 10), [11, 4]),
    ("example-2", (4, 8, 9), [12, 1]),
    ("example-3", (1, 10, 10), [11, 0]),
    ("example-4", (2, 11, 5), [7, 0]),
]

failures = 0
for label, args, claimed in witnesses:
    number, need, remaining = args
    bounded = all(0 <= value <= 1000 for value in args)
    enough = need <= remaining
    insufficient = remaining < need
    precondition = (
        bounded
        and (enough if label == "symbolic-enough" else True)
        and (insufficient if label == "symbolic-insufficient" else True)
    )
    canonical_result = canonical.eat(*args)
    solution_result = solution.eat(*args)
    ok = (
        precondition
        and canonical_result == claimed
        and solution_result == claimed
    )
    failures += not ok
    print(
        f"{label}: args={args} bounded={bounded} enough={enough} "
        f"insufficient={insufficient} precondition={precondition} "
        f"claimed={claimed} canonical={canonical_result} "
        f"solution={solution_result} pass={ok}"
    )

print(f"witnesses={len(witnesses)} failures={failures}")
raise SystemExit(1 if failures else 0)
