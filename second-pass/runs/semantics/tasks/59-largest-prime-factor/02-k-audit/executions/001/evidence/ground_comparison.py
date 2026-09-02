#!/usr/bin/env python3
"""Compare concrete claimed lpfSpec instances with both Python programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(
    "canonical_ground", "/tmp/audit-work/review-59/trusted/canonical.py"
).largest_prime_factor
solution = load(
    "solution_ground", "/tmp/audit-work/review-59/candidate-src/solution.py"
).largest_prime_factor


def lpf_spec(n: int, factor: int) -> int:
    while n > factor:
        remainder = n % factor
        if remainder == 0:
            n = (n - remainder) // factor
        else:
            factor += 1
    return factor


rows = []
for n in [12, 2048, 13195]:
    row = {
        "n": n,
        "factor": 2,
        "lpfSpec": lpf_spec(n, 2),
        "canonical": canonical(n),
        "solution": solution(n),
    }
    rows.append(row)
    if len(set(row[key] for key in ("lpfSpec", "canonical", "solution"))) != 1:
        raise SystemExit(json.dumps(row, sort_keys=True))

print(json.dumps(rows, sort_keys=True))
print("mismatch_count=0")
