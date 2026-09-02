#!/usr/bin/env python3
"""Targeted CPython recursion-boundary comparison."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


root = Path("/tmp/audit-work")
canonical = load("canonical_recursion_boundary", root / "reference/canonical.py")
candidate = load("candidate_recursion_boundary", root / "candidate/solution.py")
print(f"python={sys.version.split()[0]}")
print(f"recursion_limit={sys.getrecursionlimit()}")

observed_divergence = False
for length in (990, 995, 1000, 1050):
    values = list(range(length))
    expected = canonical(list(values))
    try:
        actual: object = candidate(list(values))
    except Exception as error:  # evidence must retain the concrete exception
        actual = f"{type(error).__name__}: {error}"
    match = actual == expected
    print(
        f"length={length} canonical_type={type(expected).__name__} "
        f"canonical_length={len(expected)} candidate={actual if not isinstance(actual, list) else 'list'} "
        f"match={match}"
    )
    if length >= 1000 and not match:
        observed_divergence = True

print(f"EXPECTED_BOUNDARY_DIVERGENCE_OBSERVED={observed_divergence}")
raise SystemExit(0 if observed_divergence else 1)
