#!/usr/bin/env python3
"""Expected outputs for the concrete K reconstruction cases."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


scratch = Path("/tmp/audit-work")
canonical = load(scratch / "trusted/canonical.py")
submitted = load(scratch / "candidate-src/solution.py")
cases = [
    "",
    "abcdef\nghijklm",
    "aeiouAEIOU",
    "zbcdf_123",
    "aBecIdOfuU",
    "éAßuİ🙂",
]

for case in cases:
    expected = canonical(case)
    actual = submitted(case)
    print(
        f"input={case!r} canonical={expected!r} "
        f"submitted={actual!r} equal={expected == actual}"
    )
    if expected != actual:
        raise SystemExit(1)
