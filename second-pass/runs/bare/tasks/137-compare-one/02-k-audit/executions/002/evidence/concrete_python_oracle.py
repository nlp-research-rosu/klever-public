#!/usr/bin/env python3
"""Python outcomes corresponding to the generated-semantics concrete cases."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


WORK = Path("/tmp/audit-work/137-compare-one-audit")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def encode(value: Any) -> dict[str, Any]:
    if isinstance(value, float):
        return {"type": "float", "repr": repr(value), "hex": value.hex()}
    return {"type": type(value).__name__, "repr": repr(value)}


def call(function, a: Any, b: Any) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": encode(function(a, b))}
    except Exception as error:
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


cases = [
    ("example_float", 1, 2.5),
    ("example_comma", 1, "2,3"),
    ("example_strings", "5,1", "6"),
    ("example_equal", "1", 1),
    ("zero_equal", -0.0, "0,0"),
    ("negative_decimal", "-0,5", 0),
    ("rational_equal", 0.1, 0.10),
    ("binary64_int_rounding", 9007199254740993, 9007199254740992),
    ("binary64_string_rounding", "9007199254740993", 9007199254740992),
    ("scientific_string", "1e2", 99),
]

canonical = load(WORK / "trusted-canonical.py", "concrete_trusted_canonical")
candidate = load(WORK / "solution.py", "concrete_candidate")
records = []
for case_id, a, b in cases:
    records.append(
        {
            "case": case_id,
            "a": encode(a),
            "b": encode(b),
            "canonical": call(canonical, a, b),
            "candidate": call(candidate, a, b),
        }
    )

print(json.dumps(records, indent=2, sort_keys=True))
if any(record["canonical"] != record["candidate"] for record in records):
    raise SystemExit(1)
