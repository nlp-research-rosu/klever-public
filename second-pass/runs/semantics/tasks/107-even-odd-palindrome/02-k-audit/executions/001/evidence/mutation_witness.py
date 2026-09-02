#!/usr/bin/env python3
"""Concrete satisfying witness for the false-postcondition mutation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


n = 3
canonical = load_entry("mutation_canonical", Path("/reference/canonical.py"))(n)
submitted = load_entry(
    "mutation_submitted", Path("/tmp/audit-work/reconstruction/solution.py")
)(n)
mutated_destination = (n // 2 + 1, (n + 1) // 2)

result = {
    "n": n,
    "precondition_1_le_n_lt_10": 1 <= n < 10,
    "canonical": canonical,
    "submitted": submitted,
    "mutated_destination": mutated_destination,
    "mutation_is_false": canonical == submitted and submitted != mutated_destination,
}
print(json.dumps(result, sort_keys=True))
raise SystemExit(0 if result["mutation_is_false"] else 1)
