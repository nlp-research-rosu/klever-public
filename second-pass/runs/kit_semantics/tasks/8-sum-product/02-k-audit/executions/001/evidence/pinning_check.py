#!/usr/bin/env python3
"""Mechanical constructor-level comparison between solution.mpy and the entry claim."""

from __future__ import annotations

import hashlib
from pathlib import Path


def extract_balanced(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start:index]
    raise ValueError(f"unbalanced expression after {marker!r}")


def strip_layout(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            result.append(character)
            in_string = True
        elif not character.isspace():
            result.append(character)
    return "".join(result)


submitted = Path("/candidate/solution.mpy").read_text()
regenerated = Path(
    "/tmp/audit-work/8-sum-product/regenerated-solution.mpy"
).read_text()
spec = Path("/candidate/spec.k").read_text()

claim_module = extract_balanced(spec, "#loadAll(")
normalized_submitted = strip_layout(submitted)
normalized_regenerated = strip_layout(regenerated)
normalized_claim = strip_layout(claim_module)

for name, term in [
    ("submitted", normalized_submitted),
    ("trusted_regenerated", normalized_regenerated),
    ("claim_load_term", normalized_claim),
]:
    print(f"{name}_length={len(term)}")
    print(f"{name}_sha256={hashlib.sha256(term.encode()).hexdigest()}")

print(f"submitted_equals_trusted_regenerated={normalized_submitted == normalized_regenerated}")
print(f"claim_load_term_equals_submitted={normalized_claim == normalized_submitted}")
print(
    "material_operations_present="
    + repr(
        {
            "ImportFrom": 'ImportFrom("typing","List","Tuple")' in normalized_claim,
            "FuncDef": 'FuncDef("sum_product",Params("numbers")' in normalized_claim,
            "sum_init": 'Assign(Name("total"),Int(0))' in normalized_claim,
            "product_init": 'Assign(Name("product"),Int(1))' in normalized_claim,
            "For": 'For(Name("number"),Name("numbers")' in normalized_claim,
            "sum_update": 'AugAssign(Name("total"),"+",Name("number"))'
            in normalized_claim,
            "product_update": 'AugAssign(Name("product"),"*",Name("number"))'
            in normalized_claim,
            "return_tuple": 'Return(TupleExpr(Name("total"),Name("product")))'
            in normalized_claim,
        }
    )
)

if not (
    normalized_submitted == normalized_regenerated
    and normalized_claim == normalized_submitted
):
    raise SystemExit(1)
