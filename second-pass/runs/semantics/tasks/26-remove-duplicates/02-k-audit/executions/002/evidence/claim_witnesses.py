#!/usr/bin/env python3
"""Ground witnesses for each entry precondition and claimed result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical")
candidate = load(
    Path("/tmp/audit-work/candidate-scratch/solution.py"), "witness_candidate"
)


def summary(acc: list[int], rest: list[int], all_values: list[int]) -> list[int]:
    output = list(acc)
    for value in rest:
        if all_values.count(value) == 1:
            output.append(value)
    return output


witnesses = [
    ("entry-empty", [], True, summary([], [], [])),
    ("entry-keep", [7], [7].count(7) == 1, summary([7], [], [7])),
    (
        "entry-drop",
        [7, 7],
        [7, 7].count(7) != 1,
        summary([], [7], [7, 7]),
    ),
    (
        "entry-keep-general",
        [1, 2, 3, 2, 4],
        [1, 2, 3, 2, 4].count(1) == 1,
        summary([1], [2, 3, 2, 4], [1, 2, 3, 2, 4]),
    ),
]

for label, values, precondition, claimed in witnesses:
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    assert precondition
    assert claimed == canonical_result == candidate_result
    print(
        f"{label}: input={values!r} precondition=true "
        f"claimed={claimed!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r}"
    )

print("claim_witnesses: PASS")
