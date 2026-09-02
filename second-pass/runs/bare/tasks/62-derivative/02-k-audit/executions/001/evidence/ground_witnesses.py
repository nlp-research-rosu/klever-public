#!/usr/bin/env python3
"""Ground witnesses used to instantiate the entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_ground", "/reference/canonical.py")
generated = load("generated_ground", "/tmp/audit-work/audit-62/solution.py")

cases = [
    [],
    [7],
    [3, 1, 2, 4, 5],
    [1, 2, 3],
    [5, -3],
    [-2, 4, -6],
]

for xs in cases:
    expected = canonical.derivative(list(xs))
    actual = generated.derivative(list(xs))
    print(f"input={xs!r} canonical={expected!r} generated={actual!r} equal={expected == actual}")
    if expected != actual:
        raise SystemExit(1)
