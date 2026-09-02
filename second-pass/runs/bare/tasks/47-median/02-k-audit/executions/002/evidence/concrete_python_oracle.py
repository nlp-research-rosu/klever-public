#!/usr/bin/env python3
"""Python-side observations for inputs used in generated-semantics smoke tests."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


path = Path("/tmp/audit-work/candidate-src/solution.py")
spec = importlib.util.spec_from_file_location("submitted_solution_concrete", path)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

huge = 10**400
cases = {
    "normal_odd": [3, 1, 2, 4, 5],
    "normal_even": [-10, 4, 6, 1000, 10, 20],
    "singleton": [7],
    "length_two": [2, 10],
    "empty": [],
    "even_four": [1, 2, 3, 4],
    "negative_odd": [-8, -1, -4],
    "even_duplicates": [5, 5, 5, 5],
    "huge_even": [huge, huge, huge, huge],
}

for name, values in cases.items():
    try:
        result = module.median(list(values))
        observation = {
            "kind": "return",
            "type": type(result).__name__,
            "value": result,
        }
    except Exception as error:
        observation = {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }
    print(json.dumps({"case": name, "input": values, "python": observation}, sort_keys=True))
