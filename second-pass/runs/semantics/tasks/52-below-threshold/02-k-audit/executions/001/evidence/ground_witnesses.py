#!/usr/bin/env python3
"""Evaluate the satisfiable ground witnesses with both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


canonical = load("ground_canonical", SCRATCH / "canonical.py")
generated = load("ground_generated", SCRATCH / "solution.py")
witnesses = [
    ([], 0, True),
    ([1, 2, 4, 10], 100, True),
    ([1, 20, 4, 10], 5, False),
    ([5], 5, False),
]

failed = False
for values, threshold, claimed in witnesses:
    oracle = canonical(list(values), threshold)
    implementation = generated(list(values), threshold)
    print(
        f"input=({values!r}, {threshold!r}) "
        f"claimed={claimed!r} canonical={oracle!r} generated={implementation!r}"
    )
    failed |= claimed != oracle or claimed != implementation
raise SystemExit(1 if failed else 0)
