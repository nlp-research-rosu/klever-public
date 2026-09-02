#!/usr/bin/env python3
"""Show that the fresh stage-6 destination is false on a satisfying input."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


x = 100
shift = 1
false_destination = "100"
assert 0 <= shift <= len(str(x))
canonical = load("stage6_canonical", Path("/reference/canonical.py"))(x, shift)
candidate = load(
    "stage6_candidate", Path("/tmp/audit-work/65-circular-shift/solution.py")
)(x, shift)
print(
    f"X={x} SHIFT={shift} len={len(str(x))} rotate_precondition=True "
    f"canonical={canonical!r} candidate={candidate!r} "
    f"false_destination={false_destination!r}"
)
assert canonical == candidate == "010"
assert canonical != false_destination
print("FALSE_WITNESS: PASS")
