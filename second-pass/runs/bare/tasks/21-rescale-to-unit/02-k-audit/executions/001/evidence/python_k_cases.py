#!/usr/bin/env python3
"""Print Python outcomes corresponding to the concrete K semantics runs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


path = Path("/tmp/audit-work/source/solution.py")
spec = importlib.util.spec_from_file_location("audit_solution_stage3", path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot import {path}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cases = {
    "prompt": [1.0, 2.0, 3.0, 4.0, 5.0],
    "two_descending": [8.0, -3.0],
    "repeated_extrema": [-5.0, -5.0, 0.0, 5.0, 5.0],
    "singleton_invalid": [1.0],
    "equal_invalid": [2.0, 2.0],
    "empty_invalid": [],
}

records = {}
for name, values in cases.items():
    try:
        records[name] = {"kind": "return", "value": module.rescale_to_unit(values)}
    except Exception as error:
        records[name] = {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }
print(json.dumps(records, indent=2, sort_keys=True))
