#!/usr/bin/env python3
"""Check satisfiable witnesses and formal branch results against both Python entries."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


def load(path: Path, name: str) -> Callable[[int, int], Any]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


canonical = load(
    Path("/tmp/audit-work/reconstruction/trusted/canonical.py"), "ground_canonical"
)
candidate = load(
    Path("/tmp/audit-work/reconstruction/solution.py"), "ground_candidate"
)


def formal_result(branch: str, n: int, m: int) -> int | str:
    total = n + m
    if branch == "inverted":
        return -1
    if branch == "integral":
        return bin(total // 2)
    lower = (total - 1) // 2
    if branch == "half-even-down":
        return bin(lower)
    if branch == "half-even-up":
        return bin(lower + 1)
    raise AssertionError(branch)


witnesses = [
    ("inverted", 2, 1),
    ("integral", 1, 3),
    ("half-even-down", 2, 3),
    ("half-even-up", 3, 4),
]

for branch, n, m in witnesses:
    expected = formal_result(branch, n, m)
    left = canonical(n, m)
    right = candidate(n, m)
    record = {
        "branch": branch,
        "n": n,
        "m": m,
        "formal_result": expected,
        "canonical": left,
        "candidate": right,
        "all_equal": expected == left == right,
    }
    print(json.dumps(record, sort_keys=True))
    if not record["all_equal"]:
        raise AssertionError(record)

print(f"witness_count={len(witnesses)} mismatches=0")
