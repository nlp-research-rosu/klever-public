#!/usr/bin/env python3
"""Concrete satisfying states and result substitutions for the three claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_divisor


canonical = load("stage4_canonical", "/reference/canonical.py")
generated = load("stage4_generated", "/tmp/audit-work/solution.py")


def first_divisor_at_or_below(n: int, d: int) -> int:
    while n % d != 0:
        d -= 1
    return d


witnesses = []
for n in [2, 15, 49]:
    d = n - 1
    expected = first_divisor_at_or_below(n, d)
    item = {
        "n": n,
        "prefix_precondition": n > 1,
        "prefix_initial_cells": {
            "env": 0,
            "scopeLoc": 1,
            "heap": {},
            "heapLoc": 0,
            "stack": [],
            "ret": "noRet",
            "exc": "NoExc",
            "exit-code": 0,
        },
        "prefix_destination_divisor": d,
        "loop_precondition": n > 1 and d >= 1 and d < n,
        "loop_initial_cells": {
            "env": 1,
            "scopeLoc": 2,
            "heap": {},
            "heapLoc": 0,
            "stack": ["frame(.K, 0, 1)"],
            "ret": "noRet",
            "exc": "NoExc",
            "exit-code": 0,
            "local_scope": {"n": n, "divisor": d, "parent": 0},
        },
        "firstDivisorAtOrBelow": expected,
        "largestProperDivisor": first_divisor_at_or_below(n, n - 1),
        "canonical": canonical(n),
        "generated": generated(n),
    }
    assert item["prefix_precondition"]
    assert item["loop_precondition"]
    assert expected == canonical(n) == generated(n)
    witnesses.append(item)

init_witness = {
    "n": 15,
    "precondition": True,
    "initial_local_scope": {"n": 15, "parent": 0},
    "destination_divisor": 14,
    "ensures": "14 == 15 - 1",
}

print(json.dumps({"init_claim": init_witness, "entry_and_loop": witnesses}, indent=2))
