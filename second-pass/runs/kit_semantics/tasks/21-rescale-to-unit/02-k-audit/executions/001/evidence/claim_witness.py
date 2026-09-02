#!/usr/bin/env python3
"""Concrete satisfying witnesses for the symbolic entry and helper claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/proof")


def load(name: str, path: Path) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


canonical = load("canonical_witness", ROOT / "canonical.py")
submitted = load("submitted_witness", ROOT / "solution.py")

# Entry-claim substitution:
# FIRST=2.0, SECOND=-2.0, REST=vCons(6.0, vCons(2.0, .ValSeq)).
values = [2.0, -2.0, 6.0, 2.0]
low = min(values)
high = max(values)
assert len(values) >= 2
assert all(type(value) is float for value in values)
assert low != high
scale_acc_interpretation = [
    (value - low) / (high - low) for value in values
]
canonical_result = canonical(values)
submitted_result = submitted(values)
assert canonical_result == scale_acc_interpretation
assert submitted_result == scale_acc_interpretation

print("entry_precondition_satisfied=yes")
print("FIRST=2.0 SECOND=-2.0 REST=[6.0, 2.0]")
print(f"interpreted_minVF={low} interpreted_maxVF={high}")
print(f"interpreted_scaleAcc={scale_acc_interpretation}")
print(f"canonical_result={canonical_result}")
print(f"submitted_result={submitted_result}")
print("claimed_return=ref(0)")
print("claimed_heap_0=list(interpreted_scaleAcc)")

# Helper-claim state witnesses. All omitted cells may be initialized exactly as
# in the supplied MPY configuration because the claims frame them.
print("min_loop_witness=VS=[2.0,-2.0,6.0], M=9.0, allFloatVS=true")
print("max_loop_witness=VS=[2.0,-2.0,6.0], M=-9.0, allFloatVS=true")
print(
    "scale_loop_witness=VS=[2.0,-2.0], ACC=[], LO=-2.0, HI=2.0, "
    "L=1, H=0, CURRENT=0.0, ORIGINAL=[2.0,-2.0], P=parent(0)"
)

for boundary in ([], [7.0], [2.0, 2.0, 2.0]):
    observed = []
    for function in (canonical, submitted):
        try:
            observed.append(("return", function(boundary)))
        except Exception as error:
            observed.append(("raise", type(error).__name__))
    assert observed[0] == observed[1]
    print(f"boundary_input={boundary} canonical_and_submitted={observed[0]}")
