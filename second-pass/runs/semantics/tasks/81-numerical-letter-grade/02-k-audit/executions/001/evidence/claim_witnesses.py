#!/usr/bin/env python3
"""Concrete witnesses for the candidate entry-claim input shapes."""

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
    return module.numerical_letter_grade


canonical = load("/reference/canonical.py", "canonical_witness")
candidate = load("/tmp/audit-work/audit-src/solution.py", "candidate_witness")

witnesses = {
    "SPEC.empty": [],
    "SPEC.a-plus": [4.0],
    "SPEC.a": [3.8],
    "SPEC.function-maps-all-numeric-grades.empty": [],
    "SPEC.function-maps-all-numeric-grades.mixed": [4.0, 3, 1.7, 0],
}

for label, values in witnesses.items():
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    print(
        json.dumps(
            {
                "claim": label,
                "input": values,
                "canonical": canonical_result,
                "candidate": candidate_result,
                "match": canonical_result == candidate_result,
            },
            sort_keys=True,
        )
    )
