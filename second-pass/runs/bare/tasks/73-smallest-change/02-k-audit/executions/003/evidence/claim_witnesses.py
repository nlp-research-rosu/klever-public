#!/usr/bin/env python3
"""Concrete satisfying witnesses for every family of submitted claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


canonical = load_function(Path("/reference/canonical.py"), "witness_canonical")
candidate = load_function(Path("/candidate/solution.py"), "witness_candidate")
witnesses = {
    "program-base and math-base": [],
    "program-equal and math-equal": [7, 7],
    "program-unequal and math-unequal": [7, 8],
    "example-one": [1, 2, 3, 5, 4, 7, 9, 6],
    "example-two": [1, 2, 3, 4, 3, 2, 2],
    "example-three": [1, 2, 3, 2, 1],
}
for claim, values in witnesses.items():
    print(
        f"{claim}: input={values!r} size={len(values)} "
        f"candidate={candidate(list(values))} canonical={canonical(list(values))}"
    )
