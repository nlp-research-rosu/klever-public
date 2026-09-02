#!/usr/bin/env python3
"""Independent Python results for the exact concrete K execution corpus."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


CASES = [
    "",
    "abAB",
    "abcCd",
    "helloE",
    "woArBld",
    "aAaaaXa",
    "@",
    "A",
    "Z",
    "[",
    "`",
    "a",
    "A@Z[",
    "É",
    "Ω",
    "𐐀",
    "aÉZΩ",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("canonical_for_krun", Path("/reference/canonical.py"))
candidate = load_module(
    "candidate_for_krun", Path("/tmp/audit-work/reconstruction/solution.py")
)

for value in CASES:
    print(
        json.dumps(
            {
                "input": value,
                "codepoints": [ord(ch) for ch in value],
                "candidate_python": candidate.digitSum(value),
                "canonical_python": canonical.digitSum(value),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
