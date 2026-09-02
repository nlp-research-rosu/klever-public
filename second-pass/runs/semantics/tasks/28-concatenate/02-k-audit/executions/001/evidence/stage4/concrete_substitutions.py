#!/usr/bin/env python3
"""Ground witnesses for each candidate claim's realizable precondition/result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/28-concatenate")


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.concatenate


canonical = load("stage4_canonical", SCRATCH / "canonical.py")
candidate = load("stage4_candidate", SCRATCH / "solution.py")

# The first is the empty entry claim, the second is the abc entry claim, and
# the remaining cases instantiate the universal loop claim at accumulator "".
cases = [
    ("entry-empty", []),
    ("entry-abc", ["a", "b", "c"]),
    ("loop-one", ["x"]),
    ("loop-empty-element", ["", "prefix", ""]),
    ("loop-general", ["left", "-", "right"]),
]

for label, strings in cases:
    expected = canonical(strings)
    actual = candidate(strings)
    assert actual == expected
    codes = [ord(character) for character in expected]
    print(
        json.dumps(
            {
                "claim_witness": label,
                "input": strings,
                "initial_accumulator": "",
                "canonical": expected,
                "candidate": actual,
                "postcondition_codes": codes,
                "precondition_all_strings": all(type(item) is str for item in strings),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
