#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import struct
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/tmp/audit-work/4mad-review/trusted-source/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/4mad-review/candidate-source/solution.py")
SEED = 0x4D4144


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def outcome(fn: Callable[[list[float]], float], values: list[float]) -> tuple[str, Any]:
    try:
        result = fn(values.copy())
    except BaseException as err:
        return ("exception", type(err).__qualname__)
    if math.isnan(result):
        return ("value", "nan")
    return ("value-bits", struct.pack(">d", result).hex())


named_cases: list[tuple[str, list[float]]] = [
    ("documented-example", [1.0, 2.0, 3.0, 4.0]),
    ("empty-boundary", []),
    ("singleton-zero", [0.0]),
    ("singleton-negative-zero", [-0.0]),
    ("singleton-positive", [7.25]),
    ("two-equal", [3.5, 3.5]),
    ("two-opposites", [-1.0, 1.0]),
    ("abs-zero-positive-negative", [-2.0, 0.0, 2.0]),
    ("all-negative", [-9.0, -4.0, -1.0]),
    ("duplicates", [1.0, 1.0, 2.0, 2.0]),
    ("fractional", [0.1, 0.2, 0.3]),
    ("large-finite", [1.0e300, -1.0e300, 1.0]),
    ("small-normal", [2.2250738585072014e-308, -2.2250738585072014e-308]),
    ("subnormal", [5.0e-324, 0.0, -5.0e-324]),
    ("positive-infinity", [math.inf]),
    ("mixed-infinities", [math.inf, -math.inf]),
    ("nan", [math.nan, 1.0]),
]

rng = random.Random(SEED)
generated_cases: list[tuple[str, list[float]]] = []
for index in range(256):
    length = rng.randint(1, 32)
    values = [rng.uniform(-1.0e6, 1.0e6) for _ in range(length)]
    generated_cases.append((f"uniform-{index}", values))
for index in range(128):
    length = rng.randint(1, 24)
    values = [
        math.ldexp(rng.uniform(-1.0, 1.0), rng.randint(-500, 500))
        for _ in range(length)
    ]
    generated_cases.append((f"wide-exponent-{index}", values))

all_cases = named_cases + generated_cases
serialized_inputs = json.dumps(
    all_cases, allow_nan=True, separators=(",", ":"), sort_keys=False
).encode()

canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "submitted_solution")

mismatches: list[dict[str, Any]] = []
for name, values in all_cases:
    expected = outcome(canonical, values)
    actual = outcome(candidate, values)
    if expected != actual:
        mismatches.append(
            {"name": name, "input": values, "canonical": expected, "candidate": actual}
        )

print(f"canonical={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"seed={SEED}")
print(f"named_cases={len(named_cases)}")
print(f"generated_cases={len(generated_cases)}")
print(f"total_cases={len(all_cases)}")
print(f"inputs_sha256={hashlib.sha256(serialized_inputs).hexdigest()}")
for name, values in named_cases:
    print(
        "named_result="
        + repr((name, values, outcome(canonical, values), outcome(candidate, values)))
    )
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("mismatch=" + repr(mismatch))

raise SystemExit(1 if mismatches else 0)
