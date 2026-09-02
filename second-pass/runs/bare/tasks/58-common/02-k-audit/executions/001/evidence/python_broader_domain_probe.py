#!/usr/bin/env python3
"""Show Python behaviors that are outside the candidate's Int-only K domain."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load(Path("/reference/canonical.py"), "canonical_broader")
generated = load(
    Path("/tmp/audit-work/58-common/solution.py"), "generated_broader"
)
cases = [
    (["b", "a", "a"], ["c", "a"]),
    ([(2,), (1,), (2,)], [(1,), (3,)]),
    ([2.5, -1.0, 2.5], [2.5, 4.0]),
]

for index, (left, right) in enumerate(cases):
    expected = canonical(left, right)
    actual = generated(left, right)
    print(
        f"CASE={index} LEFT={left!r} RIGHT={right!r} "
        f"CANONICAL={expected!r} GENERATED={actual!r} MATCH={expected == actual}"
    )
    if expected != actual:
        raise SystemExit(1)
print(f"CASE_COUNT={len(cases)} MISMATCH_COUNT=0")
