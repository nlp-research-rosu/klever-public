#!/usr/bin/env python3
"""Ground instances of the K postcondition, compared with both Python entries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "canonical_ground")
candidate = load(
    Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_ground"
)


def remove_repeated(input_values, original_values):
    """Ground reading of verification.k:11-17."""
    result = []
    for value in input_values:
        count = sum(1 for original in original_values if original == value)
        if count == 1:
            result.append(value)
    return result


cases = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [1, 2, 3, 2, 4],
    [-1, 0, -1, 2],
    [1, 2, 3, 1, 4, 2, 5],
]

for values in cases:
    claimed = remove_repeated(values, values)
    canonical_result = canonical(values)
    candidate_result = candidate(values)
    print(
        f"input={values!r} "
        f"K-postcondition={claimed!r} "
        f"canonical={canonical_result!r} "
        f"candidate={candidate_result!r}"
    )
    assert claimed == canonical_result == candidate_result
