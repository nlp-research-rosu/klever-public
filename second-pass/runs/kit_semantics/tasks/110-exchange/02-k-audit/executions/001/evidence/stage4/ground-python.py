#!/usr/bin/env python3
"""Compare both Python implementations on the ground K witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/scratch/proof")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


canonical = load(WORK / "canonical.py", "canonical_ground")
candidate = load(WORK / "solution.py", "candidate_ground")
left = [1]
right = [2]
print(f"input=({left!r}, {right!r})")
print(f"canonical={canonical(left, right)!r}")
print(f"candidate={candidate(left, right)!r}")
print("claimed_exchangeResult='YES'")
assert canonical(left, right) == candidate(left, right) == "YES"
