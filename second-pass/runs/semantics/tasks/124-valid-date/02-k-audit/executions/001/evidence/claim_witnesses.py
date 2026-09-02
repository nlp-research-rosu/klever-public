#!/usr/bin/env python3
"""Ground substitutions for both symbolic entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


canonical = load("canonical_witness", Path("/reference/canonical.py"))
generated = load(
    "generated_witness", Path("/tmp/audit-work/reconstruction/solution.py")
)


def formal_post(value: str) -> bool:
    if len(value) != 10:
        return False
    codes = tuple(ord(char) for char in value)
    m0, m1, sep1, d0, d1, sep2, y0, y1, y2, y3 = codes
    digit = lambda code: 48 <= code <= 57
    month = (m0 - 48) * 10 + m1 - 48
    day = (d0 - 48) * 10 + d1 - 48
    limit = 29 if month == 2 else 30 if month in (4, 6, 9, 11) else 31
    return (
        sep1 == 45
        and sep2 == 45
        and all(digit(code) for code in (m0, m1, d0, d1, y0, y1, y2, y3))
        and 1 <= month <= 12
        and 1 <= day <= limit
    )


witnesses = [
    ("claim1_len_not_10", ""),
    ("claim2_true", "03-11-2000"),
    ("claim2_false", "02-30-2000"),
    ("claim2_prompt_boundary", "04-30-2000"),
]

for label, value in witnesses:
    codes = [ord(char) for char in value]
    print(
        f"{label}: value={value!r} len={len(value)} codes={codes} "
        f"formal_post={formal_post(value)} "
        f"generated={generated(value)} canonical={canonical(value)}"
    )
