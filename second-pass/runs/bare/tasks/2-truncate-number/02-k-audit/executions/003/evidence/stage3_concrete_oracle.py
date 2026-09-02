#!/usr/bin/env python3
"""Independent Python results for the canonical encodings used by K runs."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "canonical_for_k")
candidate = load(Path("/tmp/audit-work/source/solution.py"), "candidate_for_k")
values = [
    3.5,
    0.25,
    1.0,
    math.nextafter(1.0, 0.0),
    math.nextafter(1.0, math.inf),
    2.0**53,
]

for value in values:
    numerator, denominator = value.as_integer_ratio()
    integer = numerator // denominator
    fraction = numerator - integer * denominator
    expected_k = (0, fraction, denominator)
    canonical_result = canonical.truncate_number(value)
    candidate_result = candidate.truncate_number(value)
    print(
        f"input={value.hex()} encoding=num({integer},{fraction},{denominator}) "
        f"expected_k=num{expected_k} canonical={canonical_result.hex()} "
        f"candidate={candidate_result.hex()} "
        f"result_ratio={candidate_result.as_integer_ratio()}"
    )
    assert canonical_result == candidate_result
    assert candidate_result.as_integer_ratio() == (fraction, denominator)

print("STAGE3_CONCRETE_ORACLE_OK")
