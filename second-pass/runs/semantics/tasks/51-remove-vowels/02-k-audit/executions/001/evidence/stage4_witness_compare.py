#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


canonical = load("stage4_canonical", "/reference/canonical.py")
candidate = load(
    "stage4_candidate",
    "/tmp/audit-work/51-remove-vowels/candidate/solution.py",
)

cases = ["", "a", "b", "abEcdU"]
rows = []
for text in cases:
    expected_codes = [
        codepoint
        for codepoint in map(ord, text)
        if codepoint not in (65, 69, 73, 79, 85, 97, 101, 105, 111, 117)
    ]
    row = {
        "input": repr(text),
        "input_codes": list(map(ord, text)),
        "formal_removeVowelCodes": expected_codes,
        "formal_string": "".join(map(chr, expected_codes)),
        "canonical": canonical(text),
        "candidate": candidate(text),
    }
    assert row["formal_string"] == row["canonical"] == row["candidate"]
    rows.append(row)

print(json.dumps(rows, indent=2, sort_keys=True))
