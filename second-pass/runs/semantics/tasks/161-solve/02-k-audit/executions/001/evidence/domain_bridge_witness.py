#!/usr/bin/env python3
"""Compare formal ground outcomes with both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_solve(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


canonical = load_solve("canonical_bridge", Path("/reference/canonical.py"))
submitted = load_solve(
    "submitted_bridge", Path("/tmp/audit-work/161-solve/source/solution.py")
)

formal_ground_outcomes = {
    "a": "A",
    "12": "21",
    # mapSwap is ASCII-only and is identity on 945/946, so the formal
    # no-letter claim reverses these code points.
    "αβ": "βα",
    # mapSwap is also identity on these uncased alphabetic code points.
    "中文": "文中",
}

for value, formal in formal_ground_outcomes.items():
    print(
        repr(value),
        "codepoints=",
        [ord(char) for char in value],
        "formal=",
        repr(formal),
        "submitted=",
        repr(submitted(value)),
        "canonical=",
        repr(canonical(value)),
    )
