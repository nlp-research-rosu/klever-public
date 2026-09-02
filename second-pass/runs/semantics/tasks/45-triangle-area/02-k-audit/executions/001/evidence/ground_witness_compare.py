#!/usr/bin/env python3
"""Compare the concrete satisfying witness A=5, H=3."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


if len(sys.argv) != 3:
    raise SystemExit("usage: ground_witness_compare.py CANONICAL GENERATED")

canonical = load(Path(sys.argv[1]), "ground_canonical")
generated = load(Path(sys.argv[2]), "ground_generated")
a, h = 5, 3
print(f"formal_precondition_witness: A={a}, H={h}")
print(f"substituted_postcondition: divII({a * h}, 2)")
print(f"independent_python_arithmetic: {a * h / 2!r}")
print(f"canonical_python: {canonical(a, h)!r}")
print(f"generated_python: {generated(a, h)!r}")
if canonical(a, h) != generated(a, h) or generated(a, h) != a * h / 2:
    raise SystemExit(1)
