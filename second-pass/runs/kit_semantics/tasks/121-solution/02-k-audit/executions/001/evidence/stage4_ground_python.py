#!/usr/bin/env python3
"""Concrete claimed-result witnesses against both Python implementations."""

from __future__ import annotations

import importlib.util
import pathlib


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
CASES = [
    ([5, 8, 7, 1], 12),
    ([3, 3, 3, 3, 3], 9),
    ([30, 13, 24, 321], 0),
    ([-3, -2, -1, 0, 1], -3),
]


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


canonical = load(WORK / "canonical.py", "stage4_canonical")
candidate = load(WORK / "solution.py", "stage4_candidate")
for values, claimed in CASES:
    canonical_result = canonical(values)
    candidate_result = candidate(values)
    print(
        f"input={values!r} claimed={claimed} "
        f"canonical={canonical_result} candidate={candidate_result}"
    )
    if canonical_result != claimed or candidate_result != claimed:
        raise SystemExit(1)
print("all_concrete_claimed_results_match=True")
