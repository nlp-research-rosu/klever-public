#!/usr/bin/env python3
"""Mechanically compare the translated function term with the spec entry term."""

from __future__ import annotations

import hashlib
from pathlib import Path


def balanced_call(text: str, start: int) -> str:
    open_paren = text.find("(", start)
    if open_paren < 0:
        raise AssertionError("constructor has no opening parenthesis")
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_paren, len(text)):
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
                return text[start : index + 1]
    raise AssertionError("unterminated constructor")


def normalize(text: str) -> str:
    """Remove insignificant whitespace while retaining quoted string bytes."""
    output: list[str] = []
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
    return "".join(output)


def main() -> None:
    solution = Path("/tmp/audit-work/case/solution.regenerated.mpy").read_text()
    spec = Path("/tmp/audit-work/case/spec.k").read_text()
    solution_start = solution.index('FuncDef("special_factorial"')
    spec_start = spec.index('FuncDef("special_factorial"')
    solution_function = normalize(balanced_call(solution, solution_start))
    spec_function = normalize(balanced_call(spec, spec_start))
    print(f"solution_function={solution_function}")
    print(f"spec_function={spec_function}")
    print(
        "solution_function_sha256="
        + hashlib.sha256(solution_function.encode()).hexdigest()
    )
    print(
        "spec_function_sha256="
        + hashlib.sha256(spec_function.encode()).hexdigest()
    )
    print(f"constructor_identity={solution_function == spec_function}")
    if solution_function != spec_function:
        raise AssertionError("entry claim executes a different function term")


if __name__ == "__main__":
    main()
