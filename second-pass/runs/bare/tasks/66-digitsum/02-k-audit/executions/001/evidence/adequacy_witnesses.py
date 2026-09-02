#!/usr/bin/env python3
"""Ground precondition/result witnesses for the two candidate claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def upper_ascii_sum(value: str) -> int:
    return sum(ord(ch) if 65 <= ord(ch) <= 90 else 0 for ch in value)


canonical = load_module("canonical_for_adequacy", Path("/reference/canonical.py"))
candidate = load_module(
    "candidate_for_adequacy", Path("/tmp/audit-work/reconstruction/solution.py")
)

for value in ("AZ", "É"):
    print(
        "ENTRY_WITNESS "
        + json.dumps(
            {
                "precondition": {
                    "k": "submitted Module(...)",
                    "input": value,
                    "env": ".Map",
                    "result": "noResult",
                },
                "formal_upperAsciiSum": upper_ascii_sum(value),
                "candidate_python": candidate.digitSum(value),
                "canonical_python": canonical.digitSum(value),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

suffix = "A@"
accumulator = 10
print(
    "LOOP_WITNESS "
    + json.dumps(
        {
            "precondition": {
                "k": "exact loopString(...) ~> execute(Return(total)) ~> .K",
                "S": suffix,
                "A": accumulator,
                "FRAME": ".Map",
                "INPUT": "",
                "result": "noResult",
                "not_total_in_FRAME": True,
            },
            "formal_result": accumulator + upper_ascii_sum(suffix),
            "candidate_suffix_plus_A": accumulator + candidate.digitSum(suffix),
            "canonical_suffix_plus_A": accumulator + canonical.digitSum(suffix),
        },
        ensure_ascii=True,
        sort_keys=True,
    )
)
