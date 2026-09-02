#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_palindrome


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(
    Path("/tmp/audit-work/48-is-palindrome/solution.py"), "generated_witness"
)

for value in ["", "aba", "zbcd", "éaé", "éaè"]:
    record = {
        "input": value,
        "IntSeq_codes": [ord(character) for character in value],
        "claimed_reverse_equality": value == value[::-1],
        "canonical": canonical(value),
        "generated": generated(value),
    }
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))
