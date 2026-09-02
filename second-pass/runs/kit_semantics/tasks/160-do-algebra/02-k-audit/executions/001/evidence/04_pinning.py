#!/usr/bin/env python3
"""Mechanical function-constructor comparison plus a concrete contract witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/160-do-algebra")


def balanced_constructor(text: str, marker: str, start: int = 0) -> str:
    begin = text.index(marker, start)
    open_paren = text.index("(", begin)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
    raise AssertionError(f"unbalanced constructor after {marker!r}")


def strip_layout(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    return "".join(output)


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


print("COMMAND: python3 /audit-output/evidence/04_pinning.py")
mpy_text = (SCRATCH / "solution.regenerated.mpy").read_text()
spec_text = (SCRATCH / "spec.k").read_text()
entry_claim_start = spec_text.index("claim [do-algebra]")
mpy_function = balanced_constructor(mpy_text, 'FuncDef("do_algebra"')
claim_function = balanced_constructor(
    spec_text, 'FuncDef(\n          "do_algebra"', entry_claim_start
)
mpy_normalized = strip_layout(mpy_function)
claim_normalized = strip_layout(claim_function)
assert mpy_normalized == claim_normalized
print("constructor_identity: PASS")
print(f"normalized_constructor_bytes={len(mpy_normalized.encode())}")
print(f"constructor={mpy_normalized}")

canonical = load_entry(Path("/reference/canonical.py"), "pinning_canonical_160")
candidate = load_entry(SCRATCH / "solution.py", "pinning_candidate_160")
operators = ["+", "*", "-"]
operands = [2, 3, 4, 5]
canonical_result = canonical(list(operators), list(operands))
candidate_result = candidate(list(operators), list(operands))
assert canonical_result == candidate_result == 9
print(f"satisfying_witness operators={operators} operands={operands}")
print("formal_precondition:")
print("  validAlgebraLists(OPERANDS, OPERATORS ++ [empty-string]) == true")
print("  OPERATORS != empty")
print(f"canonical_result={canonical_result} candidate_result={candidate_result}")
print("RESULT: PASS")
