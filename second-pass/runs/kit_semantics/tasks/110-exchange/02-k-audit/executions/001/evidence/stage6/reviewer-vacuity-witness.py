#!/usr/bin/env python3
"""Show that the false K postcondition is false on a satisfying input."""

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


canonical = load(WORK / "canonical.py", "canonical_vacuity")
candidate = load(WORK / "solution.py", "candidate_vacuity")
left = [2]
right = [1]
print("original_precondition=allNumbers([2]) and allNumbers([1]) and lengths>0")
print(f"canonical={canonical(left, right)!r}")
print(f"candidate={candidate(left, right)!r}")
print("mutated_postcondition='NO'")
assert canonical(left, right) == candidate(left, right) == "YES"
