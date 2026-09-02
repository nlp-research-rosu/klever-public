#!/usr/bin/env python3
"""Compare a satisfying formal witness and an adequacy-boundary witness."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


canonical = load_entry(
    "trusted_canonical_ground", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_entry(
    "candidate_ground", Path("/tmp/audit-work/candidate-src/solution.py")
)


def formal_model(value: str) -> list[str]:
    codes = [32 if code == 44 else code for code in map(ord, value)]
    whitespace = {9, 10, 13, 32}
    tokens: list[list[int]] = []
    current: list[int] = []
    for code in codes:
        if code in whitespace:
            if current:
                tokens.append(current)
                current = []
        else:
            current.append(code)
    if current:
        tokens.append(current)
    return ["".join(map(chr, token)) for token in tokens]


for label, value in (
    ("satisfying_ground_claim", "a,,b"),
    ("formfeed_adequacy_boundary", "\fa"),
    ("unicode_space_adequacy_boundary", "a\u2003b"),
):
    record = {
        "label": label,
        "input": value,
        "codepoints": [ord(char) for char in value],
        "formal_claim_result": formal_model(value),
        "canonical_result": canonical(value),
        "candidate_result": candidate(value),
    }
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))
