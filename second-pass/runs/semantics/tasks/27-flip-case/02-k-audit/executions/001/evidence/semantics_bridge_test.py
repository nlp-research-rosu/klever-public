#!/usr/bin/env python3
"""Compare the supplied ASCII case-map equations with Python Unicode swapcase."""

from __future__ import annotations

import json


def supplied_swap_one(code_point: int) -> str:
    if 65 <= code_point <= 90:
        code_point += 32
    elif 97 <= code_point <= 122:
        code_point -= 32
    return chr(code_point)


mismatches: list[dict[str, object]] = []
ascii_mismatches = 0
unicode_mismatches = 0
for code_point in range(0x110000):
    value = chr(code_point)
    supplied = supplied_swap_one(code_point)
    python = value.swapcase()
    if supplied != python:
        if code_point < 128:
            ascii_mismatches += 1
        else:
            unicode_mismatches += 1
        if len(mismatches) < 12:
            mismatches.append(
                {
                    "code_point": f"U+{code_point:04X}",
                    "input": repr(value),
                    "supplied_model": repr(supplied),
                    "python_swapcase": repr(python),
                }
            )

result = {
    "scope": "every one-code-point Python string",
    "ascii_mismatch_count": ascii_mismatches,
    "non_ascii_mismatch_count": unicode_mismatches,
    "first_mismatches": mismatches,
    "named_witnesses": {
        "U+00E9": {
            "input": "é",
            "supplied_model": supplied_swap_one(0x00E9),
            "python_swapcase": "é".swapcase(),
        },
        "U+00DF": {
            "input": "ß",
            "supplied_model": supplied_swap_one(0x00DF),
            "python_swapcase": "ß".swapcase(),
        },
    },
}
print(json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True))
raise SystemExit(0 if ascii_mismatches == 0 and unicode_mismatches > 0 else 1)
