#!/usr/bin/env python3
"""Ground witnesses for every target-claim precondition and result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_solution_witness",
    Path("/tmp/audit-work/92-any-int-audit/solution.py"),
)


def any_sum(x: int, y: int, z: int) -> bool:
    return x + y == z or x + z == y or y + z == x


witnesses = [
    ("int-int-int", (5, 2, 7), any_sum(5, 2, 7)),
    ("int-int-bool", (1, 0, True), any_sum(1, 0, int(True))),
    ("int-bool-int", (1, True, 2), any_sum(1, int(True), 2)),
    ("int-bool-bool", (1, False, True), any_sum(1, int(False), int(True))),
    ("bool-int-int", (True, 1, 2), any_sum(int(True), 1, 2)),
    ("bool-int-bool", (True, 0, True), any_sum(int(True), 0, int(True))),
    ("bool-bool-int", (True, True, 2), any_sum(int(True), int(True), 2)),
    ("bool-bool-bool", (False, False, False), any_sum(0, 0, 0)),
    ("float-any-any", (1.0, 1, 2), False),
    ("int-float-any", (1, 1.0, 2), False),
    ("bool-float-any", (True, 1.0, 2), False),
    ("int-int-float", (1, 2, 3.0), False),
    ("int-bool-float", (1, True, 2.0), False),
    ("bool-int-float", (True, 1, 2.0), False),
    ("bool-bool-float", (True, True, 2.0), False),
]

failures = []
for label, args, claimed in witnesses:
    canonical_result = canonical(*args)
    candidate_result = candidate(*args)
    passed = canonical_result == candidate_result == claimed
    print(
        f"{'PASS' if passed else 'FAIL'} {label}: args={args!r} "
        f"claimed={claimed!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r}"
    )
    if not passed:
        failures.append(label)

print(f"WITNESS_SUMMARY total={len(witnesses)} failures={len(failures)}")
raise SystemExit(1 if failures else 0)
