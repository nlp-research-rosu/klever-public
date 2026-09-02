#!/usr/bin/env python3
"""Mechanically extract the closure body executed by SPEC.pluck-entry."""

from __future__ import annotations

import hashlib
from pathlib import Path


WORK = Path("/tmp/audit-work/68-pluck")


def extract_balanced_call(text: str, call_start: int) -> str:
    open_paren = text.index("(", call_start)
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(open_paren, len(text)):
        char = text[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[call_start : index + 1]
    raise AssertionError("unbalanced call")


def top_level_args(call: str) -> list[str]:
    inner = call[call.index("(") + 1 : -1]
    args: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(inner):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(inner[start:index].strip())
            start = index + 1
    args.append(inner[start:].strip())
    return args


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    solution_text = (WORK / "solution.mpy").read_text()
    spec_text = (WORK / "spec.k").read_text()

    func_start = solution_text.index('FuncDef("pluck"')
    func_call = extract_balanced_call(solution_text, func_start)
    func_args = top_level_args(func_call)
    assert len(func_args) == 3
    assert "".join(func_args[0].split()) == '"pluck"'
    assert "".join(func_args[1].split()) == 'Params("arr")'

    binding = '"pluck" |-> closureVal('
    binding_start = spec_text.index(binding)
    closure_start = spec_text.index("closureVal(", binding_start)
    closure_call = extract_balanced_call(spec_text, closure_start)
    closure_args = top_level_args(closure_call)
    assert len(closure_args) == 3
    assert "".join(closure_args[0].split()) == '"arr"'
    assert "".join(closure_args[2].split()) == "0"

    body_as_program_syntax = closure_args[1]
    for internal_empty in (".Stmts", ".Exprs", ".ParamNames"):
        body_as_program_syntax = body_as_program_syntax.replace(internal_empty, "")
    extracted = (
        'Module(FuncDef("pluck", Params("arr"),\n'
        + body_as_program_syntax
        + "))\n"
    )
    extracted_path = WORK / "claim-extracted-program.mpy"
    extracted_path.write_text(extracted)

    print("binding_name=pluck")
    print("closure_parameter=arr")
    print("closure_definition_scope=0")
    print(f"solution_source_sha256={digest(WORK / 'solution.mpy')}")
    print(f"claim_extracted_source_sha256={digest(extracted_path)}")
    print(f"claim_extracted_path={extracted_path}")


if __name__ == "__main__":
    main()
