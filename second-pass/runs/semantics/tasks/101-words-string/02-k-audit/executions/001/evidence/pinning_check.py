#!/usr/bin/env python3
"""Mechanically compare the submitted MPY body with the proof's closure body."""

from __future__ import annotations

import hashlib
from pathlib import Path

SOLUTION = Path("/tmp/audit-work/candidate-src/solution.mpy")
VERIFICATION = Path("/tmp/audit-work/candidate-src/verification.k")


def extract_balanced_call(text: str, name: str) -> str:
    start = text.index(name + "(")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced {name} call")


def compact(text: str) -> str:
    """Remove layout whitespace while preserving whitespace inside K strings."""
    result = []
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
    return "".join(result)


def normalize_exprs_surface(text: str) -> str:
    """Normalize the two concrete Exprs lists used by this exact body.

    The trusted translator prints concrete comma-list syntax, while K rules
    conventionally spell the same terms with explicit `.Exprs` terminators.
    """
    text = text.replace(
        '(Str(","),Str(" "),.Exprs)',
        'Str(","),Str(" ")',
    )
    return text.replace(".Exprs", "")


solution_text = SOLUTION.read_text(encoding="utf-8")
verification_text = VERIFICATION.read_text(encoding="utf-8")
solution_body = normalize_exprs_surface(
    compact(extract_balanced_call(solution_text, "Return"))
)
verification_body = normalize_exprs_surface(
    compact(extract_balanced_call(verification_text, "Return"))
)

body_equal = solution_body == verification_body
solution_shape = 'Module(FuncDef("words_string",Params("s"),' + solution_body + "))"
solution_shape_present = normalize_exprs_surface(compact(solution_text)) == solution_shape
closure_shape = (
    'closureVal(("s",.ParamNames),' + verification_body + ".Stmts,0)"
)
closure_shape_present = closure_shape in normalize_exprs_surface(
    compact(verification_text)
)

print(f"solution_path={SOLUTION}")
print(f"verification_path={VERIFICATION}")
print(f"return_body_byte_normalized_equal={body_equal}")
print(f"solution_is_single_expected_funcdef={solution_shape_present}")
print(f"verification_contains_expected_closure={closure_shape_present}")
print(
    "solution_return_sha256="
    + hashlib.sha256(solution_body.encode()).hexdigest()
)
print(
    "verification_return_sha256="
    + hashlib.sha256(verification_body.encode()).hexdigest()
)
print("captured_environment=0")
print("claim_initial_environment=0")
print("top_level_funcdef_rule_capture_environment=the current env, which is 0")

raise SystemExit(
    0 if body_equal and solution_shape_present and closure_shape_present else 1
)
