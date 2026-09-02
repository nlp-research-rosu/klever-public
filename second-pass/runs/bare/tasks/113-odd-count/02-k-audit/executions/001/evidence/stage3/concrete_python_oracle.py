#!/usr/bin/env python3
"""Run the same concrete case classes through both independent Python entries."""

from __future__ import annotations

import importlib.util
import json
import pathlib


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, pathlib.Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


canonical = load("canonical", "/tmp/audit-work/trusted/canonical.py")
generated = load("generated", "/tmp/audit-work/source/solution.py")
cases = {
    "empty-list": [],
    "empty-string": [""],
    "prompt-one": ["1234567"],
    "parity-boundaries": ["24680", "13579"],
}

for name, value in cases.items():
    left = canonical(value)
    right = generated(value)
    print(
        json.dumps(
            {
                "case": name,
                "input": value,
                "canonical": left,
                "generated": right,
                "match": left == right,
            },
            sort_keys=True,
        )
    )
    if left != right:
        raise SystemExit(1)
