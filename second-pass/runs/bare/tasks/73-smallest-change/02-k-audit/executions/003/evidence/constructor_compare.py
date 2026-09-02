#!/usr/bin/env python3
"""Mechanically compare the submitted .mpy body with the proof abbreviation."""

from __future__ import annotations

from pathlib import Path


def normalize_k_surface(text: str) -> str:
    """Drop whitespace outside strings and normalize explicit empty Stmts."""
    text = text.replace(".Stmts", "")
    result: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    if in_string:
        raise ValueError("unterminated K String")
    return "".join(result)


solution_path = Path("/candidate/solution.mpy")
verification_path = Path("/candidate/verification.k")
solution = solution_path.read_text()
verification = verification_path.read_text()
marker = "rule #smallestChangeBody =>"
if verification.count(marker) != 1:
    raise AssertionError("expected one #smallestChangeBody equation")
body = verification.split(marker, 1)[1].rsplit("endmodule", 1)[0].strip()
constructed_module = (
    'Module(FuncDef("smallest_change", Params("arr"), ' + body + "))"
)
actual_normalized = normalize_k_surface(solution)
constructed_normalized = normalize_k_surface(constructed_module)
print(f"solution_mpy={solution_path}")
print(f"verification_body_source={verification_path}")
print(f"actual_normalized_length={len(actual_normalized)}")
print(f"constructed_normalized_length={len(constructed_normalized)}")
print(f"constructor_terms_equal={actual_normalized == constructed_normalized}")
if actual_normalized != constructed_normalized:
    print(f"actual={actual_normalized}")
    print(f"constructed={constructed_normalized}")
raise SystemExit(0 if actual_normalized == constructed_normalized else 1)
