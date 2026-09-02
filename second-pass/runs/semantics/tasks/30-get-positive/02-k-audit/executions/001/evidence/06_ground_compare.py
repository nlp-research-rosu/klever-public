#!/usr/bin/env python3
"""Evaluate the chosen satisfiable ground witness in both Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


values = [-2, 0, 3, 1]
canonical = load_entry("ground_canonical", Path("/reference/canonical.py"))
submitted = load_entry(
    "ground_submitted",
    Path("/tmp/audit-work/30-get-positive/solution.py"),
)

canonical_result = canonical(list(values))
submitted_result = submitted(list(values))
expected = [3, 1]

print(f"input={values!r}")
print(f"canonical={canonical_result!r}")
print(f"submitted={submitted_result!r}")
print(f"claimed_k_val_seq=vCons(3, vCons(1, .ValSeq))")
print(f"expected={expected!r}")

if canonical_result != expected or submitted_result != expected:
    raise SystemExit(1)

