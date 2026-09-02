#!/usr/bin/env python3
"""Concrete witnesses for both entry-claim preconditions and postconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


canonical = load("canonical_for_ground", "/reference/canonical.py")
generated = load(
    "generated_for_ground", "/tmp/audit-work/review-83/solution.py"
)


def claimed_helper(n: int) -> int:
    if n == 1:
        return 1
    assert n > 1
    decimal_middles = 10 ** (n - 2)
    starts = 10 * decimal_middles
    ends = 9 * decimal_middles
    intersection = decimal_middles
    return starts + ends - intersection


rows = []
for claim, precondition, n in [
    ("positive-n-one", "n = 1", 1),
    ("positive-n-gt-one", "n > 1", 2),
]:
    row = {
        "claim": claim,
        "precondition": precondition,
        "satisfying_input": n,
        "claimed_helper": claimed_helper(n),
        "canonical_python": canonical(n),
        "generated_python": generated(n),
    }
    row["all_equal"] = len(
        {row["claimed_helper"], row["canonical_python"], row["generated_python"]}
    ) == 1
    rows.append(row)

print(json.dumps(rows, indent=2, sort_keys=True))
raise SystemExit(0 if all(row["all_equal"] for row in rows) else 1)
