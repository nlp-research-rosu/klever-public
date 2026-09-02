#!/usr/bin/env python3
"""Check byte/AST/body identity links without trusting candidate helper scripts."""

from __future__ import annotations

import ast
from pathlib import Path
import re


WORK = Path("/tmp/audit-work/142-sum-squares")
SOLUTION_PY = WORK / "solution.py"
SOLUTION_MPY = WORK / "solution.mpy"
REGENERATED_MPY = WORK / "solution.regenerated.mpy"
SPEC = WORK / "spec.k"
CONCRETE_AUDIT = Path("/audit-output/evidence/concrete_audit.py")


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def call_arguments(text: str, marker: str, occurrence: int = 0) -> list[str]:
    positions: list[int] = []
    search_from = 0
    while True:
        position = text.find(marker, search_from)
        if position < 0:
            break
        positions.append(position)
        search_from = position + len(marker)
    if occurrence >= len(positions):
        raise AssertionError(f"missing occurrence {occurrence} of {marker}")
    start = positions[occurrence] + len(marker)
    depth = 0
    quoted = False
    escaped = False
    argument_start = start
    arguments: list[str] = []
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
            if depth == 0:
                arguments.append(text[argument_start:index])
                return arguments
            depth -= 1
        elif character == "," and depth == 0:
            arguments.append(text[argument_start:index])
            argument_start = index + 1
    raise AssertionError(f"unterminated call after {marker}")


submitted = SOLUTION_MPY.read_bytes()
regenerated = REGENERATED_MPY.read_bytes()
assert submitted == regenerated, "submitted and trusted-regenerated MPY differ"

solution_tree = ast.parse(SOLUTION_PY.read_text(encoding="utf-8"))
concrete_tree = ast.parse(CONCRETE_AUDIT.read_text(encoding="utf-8"))
solution_function = solution_tree.body[0]
concrete_function = concrete_tree.body[0]
assert isinstance(solution_function, ast.FunctionDef)
assert isinstance(concrete_function, ast.FunctionDef)
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    concrete_function, include_attributes=False
), "concrete audit function is not the exact candidate function AST"

module = compact(submitted.decode("utf-8"))
prefix = 'Module(FuncDef("sum_squares",Params("lst"),'
assert module.startswith(prefix), "translated MPY has unexpected entry prefix"
assert module.endswith("))"), "translated MPY has unexpected suffix"
function_body = module[len(prefix) : -2]

expected_closure = f'closureVal("lst",{function_body},0)'
spec = compact(SPEC.read_text(encoding="utf-8"))
assert spec.count(expected_closure) == 1, (
    "entry claim does not contain exactly one exact translated closure body"
)
expected_call = 'Call(Name("sum_squares"),list(VS:ValSeq))'
assert spec.count(expected_call) == 1, (
    "entry claim does not execute exactly the required symbolic call"
)

for_arguments = call_arguments(function_body, "For(")
assert len(for_arguments) == 3
assert for_arguments[0] == 'Name("value")'
assert for_arguments[1] == 'Name("lst")'
loop_arguments = call_arguments(spec, "#loop(")
assert len(loop_arguments) == 3
assert loop_arguments[0] == "list(VS:ValSeq)"
assert loop_arguments[1] == 'Name("value")'
assert loop_arguments[2] == for_arguments[2], (
    "loop claim body differs from the exact translated For body"
)

print("submitted-vs-trusted-regenerated-mpy: BYTE_IDENTICAL")
print("concrete-audit-vs-solution-function: AST_IDENTICAL")
print("entry-closure-vs-translated-function-body: EXACTLY_ONE")
print("entry-call: EXACTLY_ONE")
print("loop-claim-body-vs-translated-For-body: EXACT")
