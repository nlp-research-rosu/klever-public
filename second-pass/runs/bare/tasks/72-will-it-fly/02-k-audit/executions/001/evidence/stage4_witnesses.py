#!/usr/bin/env python3
"""Concrete satisfying states for all five entry claims."""

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
    return module.will_it_fly


scratch = Path(sys.argv[1]).resolve()
canonical = load(scratch / "trusted-canonical.py", "trusted_canonical")
generated = load(scratch / "solution.py", "generated_solution")

states = [
    ("universal@IS=[2,-5,2],W=-1", [2, -5, 2], -1, True),
    ("example-unbalanced", [1, 2], 5, False),
    ("example-overweight", [3, 2, 3], 1, False),
    ("example-balanced", [3, 2, 3], 9, True),
    ("example-singleton", [3], 5, True),
]

for label, q, w, claimed in states:
    formula = q == list(reversed(q)) and sum(q) <= w
    oracle = canonical(q, w)
    subject = generated(q, w)
    print(
        f"{label}: q={q!r} w={w} "
        f"claim={claimed!r} formula={formula!r} "
        f"canonical={oracle!r} generated={subject!r}"
    )
    if not (claimed is formula is oracle is subject):
        raise AssertionError(label)
