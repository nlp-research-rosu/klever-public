#!/usr/bin/env python3
"""Concrete satisfying witnesses for every end-to-end entry claim in spec.k."""

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


canonical = load("canonical_entry", "/tmp/audit-work/trusted/canonical.py")
generated = load("generated_entry", "/tmp/audit-work/source/solution.py")

witnesses = [
    ("empty-list", [], "pyList(noValues)"),
    (
        "prompt-example-one",
        ["1234567"],
        "pyList(value(pyString(inputDigits(O,E,O,E,O,E,O)),noValues))",
    ),
    (
        "prompt-example-two",
        ["3", "11111111"],
        "pyList(value(pyString(inputDigits(O)),"
        "value(pyString(inputDigits(O,O,O,O,O,O,O,O)),noValues)))",
    ),
]

for claim, concrete_input, abbreviated_k_input in witnesses:
    canonical_result = canonical(concrete_input)
    generated_result = generated(concrete_input)
    print(
        json.dumps(
            {
                "claim": claim,
                "concrete_input": concrete_input,
                "formal_input_abbreviation": abbreviated_k_input,
                "canonical_result": canonical_result,
                "generated_result": generated_result,
                "matches": canonical_result == generated_result,
            },
            sort_keys=True,
        )
    )
    if canonical_result != generated_result:
        raise SystemExit(1)
