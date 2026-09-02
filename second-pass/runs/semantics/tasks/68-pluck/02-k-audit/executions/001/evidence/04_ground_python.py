#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


canonical = load("/reference/canonical.py", "canonical_ground")
generated = load("/tmp/audit-work/68-pluck/solution.py", "generated_ground")
cases = [
    [],
    [4, 2, 3],
    [5, 0, 3, 0, 4, 2],
    [7, 5, 9],
    [6, 2, 9, 2],
    [9, 7, 0],
]
for values in cases:
    expected = canonical(list(values))
    actual = generated(list(values))
    print(f"input={values!r} canonical={expected!r} generated={actual!r}")
    if expected != actual:
        raise SystemExit(1)
