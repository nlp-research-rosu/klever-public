#!/usr/bin/env python3
"""Concrete Python oracle outputs corresponding to the audited krun cases."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


canonical = load(
    "/tmp/audit-work/104-unique-digits/reference/canonical.py", "canonical_cases"
)
candidate = load(
    "/tmp/audit-work/104-unique-digits/candidate/solution.py", "candidate_cases"
)

cases = {
    "empty": [],
    "base_and_even": [1, 2],
    "example_one": [15, 33, 1422, 1],
    "example_two": [152, 323, 1422, 10],
    "duplicates": [97531, 7, 111, 97531],
}

for name, values in cases.items():
    expected = canonical(values.copy())
    actual = candidate(values.copy())
    print(
        json.dumps(
            {
                "case": name,
                "input": values,
                "canonical": expected,
                "candidate": actual,
                "match": expected == actual,
            },
            sort_keys=True,
        )
    )
