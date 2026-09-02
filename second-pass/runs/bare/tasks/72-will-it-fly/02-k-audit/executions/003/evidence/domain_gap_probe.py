#!/usr/bin/env python3
"""Concrete witnesses in the prompt's numeric domain but outside the K claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/72-will-it-fly-audit")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


canonical = load(ROOT / "reference/canonical.py", "gap_canonical")
generated = load(ROOT / "candidate/solution.py", "gap_generated")

cases = [
    ([0.25, 0.5, 0.25], 1.0),
    ([0.25, 0.5, 0.25], 0.9),
    ([1], 1.5),
    ([-0.25, -0.25], -0.5),
]

for q, w in cases:
    expected = canonical(list(q), w)
    actual = generated(list(q), w)
    assert actual is expected
    print(f"q={q!r} w={w!r} canonical={expected} generated={actual}")

print("K representability: none; Val has pyList(IntList) and pyInt(Int), no float value.")
