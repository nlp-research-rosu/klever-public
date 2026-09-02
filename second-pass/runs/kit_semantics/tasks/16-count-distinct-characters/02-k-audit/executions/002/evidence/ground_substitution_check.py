#!/usr/bin/env python3
"""Evaluate concrete substitutions of the claim's supplied-model result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


def supplied_model_postcondition(text: str) -> int:
    # str.k lowerC: ASCII A-Z map to a-z; every other code is unchanged.
    lowered_codes = [
        code + 32 if 65 <= code <= 90 else code for code in map(ord, text)
    ]
    deduplicated: list[int] = []
    for code in lowered_codes:
        if code not in deduplicated:
            deduplicated.append(code)
    return len(deduplicated)


canonical = load_entry("ground_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "ground_generated", Path("/tmp/audit-work/candidate-src/solution.py")
)

model_representable_witnesses = ["", "xyzXYZ", "Jerry", "aA", "ABCabc", "\x00"]
for text in model_representable_witnesses:
    claimed = supplied_model_postcondition(text)
    canonical_result = canonical(text)
    generated_result = generated(text)
    print(
        f"input={text!r} claim={claimed} canonical={canonical_result} "
        f"generated={generated_result}"
    )
    assert claimed == canonical_result == generated_result

gap = "İ"
print(
    f"gap={gap!r} claim={supplied_model_postcondition(gap)} "
    f"canonical={canonical(gap)} generated={generated(gap)} "
    f"cpython_lower_codes={[ord(c) for c in gap.lower()]}"
)
assert supplied_model_postcondition(gap) == 1
assert canonical(gap) == generated(gap) == 2
