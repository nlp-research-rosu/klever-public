#!/usr/bin/env python3

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


canonical = load("/reference/canonical.py", "canonical_ground")
generated = load("/tmp/audit-work/source/solution.py", "generated_ground")
inputs = [
    [],
    ["1234567"],
    ["3", "11111111"],
    ["1111111111"],
]
records = []
for case in inputs:
    expected = canonical(case)
    actual = generated(case)
    records.append(
        {
            "input": case,
            "canonical": expected,
            "generated": actual,
            "equal": expected == actual,
        }
    )

print(json.dumps(records, indent=2, ensure_ascii=True))
raise SystemExit(0 if all(record["equal"] for record in records) else 1)
