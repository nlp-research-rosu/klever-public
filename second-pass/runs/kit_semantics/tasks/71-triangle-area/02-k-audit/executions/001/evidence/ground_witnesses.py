#!/usr/bin/env python3
"""Exhibit a ground satisfying witness for each of the 27 entry claims."""

from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path
from typing import Any


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


candidate = load("/tmp/audit-work/proof/solution.py", "ground_candidate")
canonical = load("/reference/canonical.py", "ground_canonical")

values: dict[str, tuple[Any, str]] = {
    "int-a": (3, "3:Int"),
    "int-b": (4, "4:Int"),
    "int-c": (5, "5:Int"),
    "float-a": (3.0, "3.0:Float"),
    "float-b": (4.0, "4.0:Float"),
    "float-c": (5.0, "5.0:Float"),
    "bool-a": (True, "true:Bool"),
    "bool-b": (True, "true:Bool"),
    "bool-c": (True, "true:Bool"),
}


def contract_result(args: tuple[Any, Any, Any]) -> Any:
    a, b, c = args
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    s = (a + b + c) / 2
    # Alternate symmetric Heron formula for the ground interpretation.
    area = math.sqrt((a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)) / 4
    return round(area, 2)


failures = 0
for sorts in itertools.product(("int", "float", "bool"), repeat=3):
    args = tuple(values[f"{sort}-{position}"][0] for sort, position in zip(sorts, "abc"))
    k_terms = tuple(values[f"{sort}-{position}"][1] for sort, position in zip(sorts, "abc"))
    label = "triangle-area-" + "-".join(sorts)
    if sorts == ("int", "int", "int"):
        label = "triangle-area-int"
    formal_ground = contract_result(args)
    candidate_ground = candidate(*args)
    canonical_ground = canonical(*args)
    agrees = formal_ground == candidate_ground == canonical_ground
    failures += not agrees
    print(
        f"CLAIM={label} K_INPUTS={k_terms!r} PY_INPUTS={args!r} "
        f"FORMAL_GROUND={formal_ground!r} CANDIDATE={candidate_ground!r} "
        f"CANONICAL={canonical_ground!r} AGREES={agrees}"
    )

print("TOTAL_WITNESSES=27")
print(f"WITNESS_FAILURES={failures}")
assert failures == 0
