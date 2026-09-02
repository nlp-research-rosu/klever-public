#!/usr/bin/env python3
"""Ground witness falsifying the reviewer-authored always-true mutation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


trusted = load_entry("trusted_vacuity", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_vacuity", Path("/tmp/audit-work/candidate-src/solution.py")
)

values: list[int] = []
print(
    f"input={values!r} trusted={trusted(values)!r} "
    f"candidate={candidate(values)!r} mutated_expected=True"
)
assert trusted(values) is False
assert candidate(values) is False
