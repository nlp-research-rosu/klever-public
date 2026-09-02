"""Concrete satisfying witnesses for the formal entry result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/135-can-arrange")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load("stage4_solution", SCRATCH / "solution.py")
canonical = load("stage4_canonical", SCRATCH / "trusted-canonical.py")


def arrange_summary(values):
    result = -1
    for index, value in enumerate(values):
        if index > 0 and not value >= values[index - 1]:
            result = index
    return result


witnesses = [
    ("empty-precondition-witness", []),
    ("documented-descent", [1, 2, 4, 3, 5]),
    ("documented-sorted", [1, 2, 3]),
    ("multiple-descents", [5, 4, 3]),
]

for name, values in witnesses:
    summary = arrange_summary(values)
    generated = candidate.can_arrange(values)
    helper = canonical.can_arrange(values)
    print(name, "scanDefined=true", "arrangeSeq=", summary,
          "generated=", generated, "canonical=", helper)
    assert summary == generated == helper
