#!/usr/bin/env python3
"""Python-side expected values for the exact K concrete-run inputs."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.concatenate


canonical = load("/reference/canonical.py", "canonical_for_krun")
generated = load("/candidate/solution.py", "candidate_for_krun")

cases = [
    [],
    [""],
    ["a", "b", "c"],
    ["", "hello", "", " world"],
    ["é", "λ", "🙂"],
]

for value in cases:
    expected = canonical(value)
    actual = generated(value)
    print(
        f"input={value!r} canonical={expected!r} "
        f"generated={actual!r} equal={expected == actual}"
    )
    if expected != actual:
        raise SystemExit(1)
