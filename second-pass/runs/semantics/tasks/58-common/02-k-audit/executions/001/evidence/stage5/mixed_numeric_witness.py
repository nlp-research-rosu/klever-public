#!/usr/bin/env python3
"""A valid Python-domain witness for cross-type numeric equality."""

import importlib.util
from pathlib import Path


def load_common(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load_common("canonical_mixed_58", Path("/reference/canonical.py"))
candidate = load_common(
    "candidate_mixed_58", Path("/tmp/audit-work/case58/solution.py")
)

cases = [
    ([True], [1]),
    ([1], [True]),
    ([1], [1.0]),
    ([False, 0, 2], [0]),
]

for left, right in cases:
    expected = canonical(left.copy(), right.copy())
    actual = candidate(left.copy(), right.copy())
    print(f"{left!r}, {right!r} -> canonical={expected!r} candidate={actual!r}")
    assert actual == expected

assert candidate([True], [1]) == [True]
