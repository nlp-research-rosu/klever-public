#!/usr/bin/env python3
"""Mechanical AST-text pinning checks between solution.mpy, spec, and bridge."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def normalized(path: Path) -> str:
    text = re.sub(r"//[^\n]*", "", path.read_text(encoding="utf-8"))
    text = re.sub(r"\s+", "", text)
    # The pretty-printer elides the terminator of an empty Stmts list, while
    # handwritten K commonly spells it `.Stmts`; both parse to the same term.
    return text.replace(".Stmts", "")


def balanced_term(text: str, constructor: str, start: int = 0) -> str:
    begin = text.index(constructor + "(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(begin + len(constructor), len(text)):
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
                return text[begin : index + 1]
    raise ValueError(f"unbalanced {constructor} term")


def constructor_args(term: str) -> list[str]:
    begin = term.index("(")
    inner = term[begin + 1 : -1]
    args = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, character in enumerate(inner):
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
        elif character == "," and depth == 0:
            args.append(inner[start:index])
            start = index + 1
    args.append(inner[start:])
    return args


solution_path = Path("/candidate/solution.mpy")
spec_path = Path("/candidate/spec.k")
verification_path = Path("/candidate/verification.k")

solution = normalized(solution_path)
spec = normalized(spec_path)
verification = normalized(verification_path)

prefix = 'Module(FuncDef("reverse_delete",Params("s","c"),'
assert solution.startswith(prefix)
assert solution.endswith("))")
body = solution[len(prefix) : -2]
expected_call = 'Call(closureVal(("s","c"),' + body + ",0),str(S:IntSeq),str(C:IntSeq))"
exact_entry_body = expected_call in spec

solution_loop = balanced_term(solution, "For")
loop_args = constructor_args(solution_loop)
assert len(loop_args) == 3
expected_evaluated_loop = (
    "#loop(str(S:IntSeq)," + loop_args[0] + "," + loop_args[2] + ")"
)
for_in_entry_claim = solution_loop in spec
loop_in_loop_claim = expected_evaluated_loop in spec
loop_in_bridge = expected_evaluated_loop in verification

report = {
    "solution_mpy_sha256": hashlib.sha256(solution_path.read_bytes()).hexdigest(),
    "spec_sha256": hashlib.sha256(spec_path.read_bytes()).hexdigest(),
    "verification_sha256": hashlib.sha256(
        verification_path.read_bytes()
    ).hexdigest(),
    "normalized_solution_body_length": len(body),
    "exact_entry_closure_call_found": exact_entry_body,
    "normalized_loop_term_length": len(solution_loop),
    "exact_for_term_found_in_entry_claim": for_in_entry_claim,
    "exact_loop_found_in_loop_claim": loop_in_loop_claim,
    "exact_loop_found_in_verification_bridge": loop_in_bridge,
}
print(json.dumps(report, indent=2))
raise SystemExit(
    0
    if (
        exact_entry_body
        and for_in_entry_claim
        and loop_in_loop_claim
        and loop_in_bridge
    )
    else 1
)
