#!/usr/bin/env python3
"""Concrete substitutions into the entry claim's scan recurrence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def claimed_scan(values: list[int]) -> bool:
    ok = True
    previous = 0
    repeats = 0
    for value in values:
        repeats = repeats + 1 if value == previous else 1
        ok = ok and previous <= value and repeats <= 2
        previous = value
    return ok


ROOT = Path("/tmp/audit-work/126-is-sorted-audit-003")
canonical = load_entry(ROOT / "canonical.py", "canonical_ground_126")
candidate = load_entry(ROOT / "solution.py", "candidate_ground_126")

intended_cases = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [1, 2, 2],
    [1, 2, 2, 2],
    [1, 0],
    [1, 3, 2, 4, 5],
]

rows = []
for values in intended_cases:
    rows.append(
        {
            "input": values,
            "claimed_scan": claimed_scan(values),
            "candidate_python": candidate(values),
            "canonical_python": canonical(values),
        }
    )

outside_domain = [-1]
summary = {
    "entry_precondition_witness": {
        "INPUT": ".IntSeq",
        "env": 0,
        "scopes": {
            "0": 'scope("is_sorted" |-> isSortedClosure, parent(-1))',
            "-1": "builtinsScope",
        },
        "scopeLoc": 1,
        "heap": ".Map",
        "heapLoc": 0,
        "stack": ".List",
        "ret": "noRet",
        "exc": "NoExc",
    },
    "loop_precondition_witness": {
        "IS": ".IntSeq",
        "OK": True,
        "PREV": 0,
        "COUNT": 0,
        "FRAME": 1,
        "SAVED": 1,
        "CURRENT": 1,
        "CALLER": 0,
        "CONT": ".K",
        "STACK": ".List",
        "LOCALS": ".Map",
        "BASE": ".Map",
        "PARENT": "parent(0)",
        "NUMBER": 0,
        "all_requires_evaluate_true": True,
    },
    "intended_domain_rows": rows,
    "intended_domain_mismatches": sum(
        not (
            row["claimed_scan"]
            == row["candidate_python"]
            == row["canonical_python"]
        )
        for row in rows
    ),
    "outside_promised_domain_observation": {
        "input": outside_domain,
        "claimed_scan": claimed_scan(outside_domain),
        "candidate_python": candidate(outside_domain),
        "canonical_python": canonical(outside_domain),
        "note": "Negative integers are explicitly excluded by the source contract.",
    },
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if summary["intended_domain_mismatches"] else 0)
