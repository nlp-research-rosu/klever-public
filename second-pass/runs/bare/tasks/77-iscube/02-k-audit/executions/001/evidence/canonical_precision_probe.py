#!/usr/bin/env python3
"""Probe the trusted floating-point canonical at exact large integer cubes."""

from __future__ import annotations

import importlib.util
from pathlib import Path

CANONICAL = Path("/reference/canonical.py")
spec = importlib.util.spec_from_file_location("trusted_canonical", CANONICAL)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot import {CANONICAL}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

roots = [
    1_000_000,
    10_000_000,
    100_000_000,
    1_000_000_000,
    1_000_000_000_000,
    1_000_000_000_000_000,
    562_949_953_421_312,
]

failures = []
for root in roots:
    value = root**3
    try:
        result = module.iscube(value)
    except Exception as exc:  # Preserve canonical exceptions as observations.
        result = f"{type(exc).__name__}: {exc}"
    print(f"root={root} digits={len(str(value))} canonical={result!r} exact=True")
    if result is not True:
        failures.append((root, result))

print(f"large_exact_cube_failure_count={len(failures)}")
print("This probe diagnoses the trusted reference; failures are not attributed to the candidate.")

