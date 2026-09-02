#!/usr/bin/env python3
"""Compare ground claim substitutions with both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


canonical = entry(Path("/reference/canonical.py"), "ground_canonical")
candidate = entry(
    Path("/tmp/audit-work/candidate-src/solution.py"), "ground_candidate"
)

witnesses = [
    ([], []),
    ([4.0, 3, 1.7, 2, 3.5], ["A+", "B", "C-", "C", "A-"]),
]
for grades, claimed in witnesses:
    canonical_value = canonical(list(grades))
    candidate_value = candidate(list(grades))
    print(
        f"grades={grades!r} claimed={claimed!r} "
        f"canonical={canonical_value!r} candidate={candidate_value!r}"
    )
    if canonical_value != claimed or candidate_value != claimed:
        raise SystemExit(1)
print("GROUND_WITNESS_PYTHON PASS")
