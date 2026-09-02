#!/usr/bin/env python3
"""Mechanical constructor-level comparison of translated and claimed bodies."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/27-flip-case")


def extract_balanced_constructor(text: str, constructor: str) -> str:
    start = text.index(constructor + "(")
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise AssertionError(f"unbalanced constructor {constructor}")


def normalize_k_list_sugar(text: str) -> str:
    compact = re.sub(r"\s+", "", text)
    # In List{Expr, ","}, an omitted final element and `.Exprs` are the same
    # empty-list constructor.
    return compact.replace(",.Exprs)", ",)")


translated = extract_balanced_constructor(
    (SCRATCH / "solution.mpy").read_text(), "FuncDef"
)
claimed = extract_balanced_constructor((SCRATCH / "spec.k").read_text(), "FuncDef")
translated_normal = normalize_k_list_sugar(translated)
claimed_normal = normalize_k_list_sugar(claimed)

print(f"translated_constructor={translated_normal}")
print(f"claimed_constructor={claimed_normal}")
print(f"constructor_equal={translated_normal == claimed_normal}")
assert translated_normal == claimed_normal
print("PROGRAM_PINNING=PASS")
