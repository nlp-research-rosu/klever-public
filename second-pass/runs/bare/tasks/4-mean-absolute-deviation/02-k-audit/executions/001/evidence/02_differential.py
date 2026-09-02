#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test.

The oracle and candidate are imported from distinct, explicit source paths.
Every input and both observed outcomes are emitted as one JSON line.
"""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def outcome(fn: Callable[[list[float]], float], values: list[float]) -> dict[str, Any]:
    try:
        value = fn(list(values))
    except Exception as error:  # comparison includes boundary exceptions
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}
    if math.isnan(value):
        rendered: Any = "NaN"
    elif math.isinf(value):
        rendered = "+Infinity" if value > 0 else "-Infinity"
    else:
        rendered = value.hex()
    return {"kind": "value", "float": rendered}


def equivalent(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["kind"] != right["kind"]:
        return False
    if left["kind"] == "exception":
        return left["type"] == right["type"]
    return left["float"] == right["float"]


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "scratch_candidate"
)

cases: list[tuple[str, list[float]]] = [
    ("documented-example", [1.0, 2.0, 3.0, 4.0]),
    ("empty-boundary", []),
    ("singleton-zero", [0.0]),
    ("singleton-negative", [-7.25]),
    ("two-equal", [3.5, 3.5]),
    ("two-opposites", [-1.0, 1.0]),
    ("negative-zero", [-0.0, 0.0]),
    ("negative-center-positive", [-2.0, 0.0, 2.0]),
    ("all-negative", [-9.0, -4.0, -1.0]),
    ("duplicates-and-center", [1.0, 1.0, 2.0, 3.0, 3.0]),
    ("fractional-exact-binary", [0.25, 0.5, 1.25, 2.0]),
    ("cancellation", [1.0e16, 1.0, -1.0e16]),
    ("tiny-normal", [sys.float_info.min, -sys.float_info.min]),
    ("tiny-subnormal", [5e-324, 0.0]),
    ("large-finite", [sys.float_info.max / 4, -(sys.float_info.max / 4)]),
    ("positive-infinity", [1.0, math.inf]),
    ("nan-element", [1.0, math.nan, 2.0]),
]

rng = random.Random(0x4D4144)
pool = [-100.0, -10.5, -1.0, -0.25, 0.0, 0.25, 1.0, 10.5, 100.0]
for index in range(100):
    length = rng.randint(1, 12)
    cases.append((f"generated-pool-{index:03d}", [rng.choice(pool) for _ in range(length)]))
for index in range(100):
    length = rng.randint(1, 12)
    cases.append(
        (
            f"generated-finite-{index:03d}",
            [rng.uniform(-1.0e6, 1.0e6) for _ in range(length)],
        )
    )

mismatches = 0
for index, (label, values) in enumerate(cases):
    canonical_result = outcome(canonical, values)
    candidate_result = outcome(candidate, values)
    matches = equivalent(canonical_result, candidate_result)
    mismatches += not matches
    print(
        json.dumps(
            {
                "index": index,
                "label": label,
                "input": values,
                "canonical": canonical_result,
                "candidate": candidate_result,
                "match": matches,
            },
            allow_nan=True,
            sort_keys=True,
        )
    )

print(
    json.dumps(
        {
            "summary": {
                "total": len(cases),
                "mismatches": mismatches,
                "seed": "0x4D4144",
            }
        },
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)

