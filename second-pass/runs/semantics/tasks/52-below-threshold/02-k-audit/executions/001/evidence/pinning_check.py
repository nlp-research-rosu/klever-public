#!/usr/bin/env python3
"""Check that proof-local body macros expand to the submitted .mpy body."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")
submitted_path = SCRATCH / "submitted-solution.mpy"
regenerated_path = SCRATCH / "regenerated-solution.mpy"
verification_path = SCRATCH / "verification.k"


def matching_paren(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unmatched parenthesis")


def constructor_args(text: str, constructor_start: int) -> list[str]:
    opening = text.index("(", constructor_start)
    closing = matching_paren(text, opening)
    inside = text[opening + 1 : closing]
    args = []
    last = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(inside):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(inside[last:index].strip())
            last = index + 1
    args.append(inside[last:].strip())
    return args


def normalize_k(text: str) -> str:
    output = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    normalized = "".join(output)
    # `.Stmts` is the explicit unit of the Stmts list.  The translator renders
    # an empty list argument as nothing after the comma; K accepts both surface
    # forms and parses them to the same term.
    return normalized.replace(",.Stmts)", ",)")


def rule_rhs(source: str, rule_name: str, end_marker: str) -> str:
    match = re.search(rf"\brule\s+{re.escape(rule_name)}\s*=>", source)
    if not match:
        raise ValueError(f"cannot find rule {rule_name}")
    end = source.index(end_marker, match.end())
    return source[match.end() : end].strip()


submitted = submitted_path.read_text()
verification = verification_path.read_text()
function_start = submitted.index('FuncDef("below_threshold"')
function_args = constructor_args(submitted, function_start)
if len(function_args) != 3:
    raise ValueError(f"expected three FuncDef arguments, got {len(function_args)}")
submitted_body = function_args[2]

for_start = submitted_body.index("For(")
for_args = constructor_args(submitted_body, for_start)
if len(for_args) != 3:
    raise ValueError(f"expected three For arguments, got {len(for_args)}")
submitted_loop_body = for_args[2]

loop_macro = rule_rhs(verification, "belowThresholdLoopBody", "syntax Stmts ::= \"belowThresholdBody\"")
body_macro = rule_rhs(verification, "belowThresholdBody", "syntax KItem ::= #belowThresholdCall")
call_macro = rule_rhs(verification, "#belowThresholdCall(IS:IntSeq, T:Int)", "endmodule")

normalized_loop_submitted = normalize_k(submitted_loop_body)
normalized_loop_macro = normalize_k(loop_macro)
expanded_body_macro = normalize_k(body_macro).replace(
    "belowThresholdLoopBody", normalized_loop_macro
)
normalized_submitted_body = normalize_k(submitted_body)

expected_call = normalize_k(
    """
    Call(
      closureVal(("l", "t", .ParamNames), belowThresholdBody, 0),
      (list(intsToVals(IS)), T, .Exprs))
    """
)
normalized_call_macro = normalize_k(call_macro)

checks = {
    "submitted_equals_trusted_regeneration": submitted_path.read_bytes()
    == regenerated_path.read_bytes(),
    "loop_macro_equals_submitted_loop_body": normalized_loop_macro
    == normalized_loop_submitted,
    "expanded_body_macro_equals_submitted_function_body": expanded_body_macro
    == normalized_submitted_body,
    "entry_macro_is_exact_direct_closure_call": normalized_call_macro == expected_call,
}

for path in (submitted_path, regenerated_path, verification_path):
    print(f"SHA256 {path} {hashlib.sha256(path.read_bytes()).hexdigest()}")
for name, result in checks.items():
    print(f"{name}={str(result).lower()}")

if not all(checks.values()):
    print("normalized submitted loop:", normalized_loop_submitted)
    print("normalized loop macro:", normalized_loop_macro)
    print("normalized submitted body:", normalized_submitted_body)
    print("normalized expanded body macro:", expanded_body_macro)
    print("normalized expected call:", expected_call)
    print("normalized call macro:", normalized_call_macro)
    sys.exit(1)
sys.exit(0)
