#!/usr/bin/env python3
"""Show the CPython recursion-resource boundary excluded by the K model."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/80-is-happy")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


canonical = load_entry(SCRATCH / "trusted-canonical.py", "resource_canonical")
generated = load_entry(SCRATCH / "solution.py", "resource_generated")

for size in [100, 900, 950, 975, 990, 995, 1000, 1100]:
    text = ("abc" * ((size + 2) // 3))[:size]
    canonical_value: object
    generated_value: object
    try:
        canonical_value = canonical(text)
    except Exception as error:  # pragma: no cover - evidence capture
        canonical_value = type(error).__name__
    try:
        generated_value = generated(text)
    except Exception as error:
        generated_value = type(error).__name__
    print(
        f"length={size} canonical={canonical_value!r} "
        f"generated={generated_value!r}"
    )
