#!/usr/bin/env python3
"""Mechanical constructor-level comparison for the submitted program and claims."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/3-below-zero-audit")


def extract_call(text: str, constructor: str, start: int = 0) -> tuple[str, int]:
    begin = text.index(constructor + "(", start)
    depth = 0
    quoted = False
    escaped = False
    for index in range(begin + len(constructor), len(text)):
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
                return text[begin : index + 1], index + 1
    raise AssertionError(f"unbalanced constructor: {constructor}")


def arguments(term: str) -> list[str]:
    inside = term[term.index("(") + 1 : -1]
    args: list[str] = []
    depth = 0
    quoted = False
    escaped = False
    last = 0
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
            args.append(inside[last:index])
            last = index + 1
    args.append(inside[last:])
    return args


def norm(text: str) -> str:
    compact = re.sub(r"\s+", "", text)
    # The translator prints the empty Stmts list in the false arm as an empty
    # concrete-list field (`,)`), while the handwritten claim spells the same K
    # list unit `.Stmts`.  Normalize that one parser-level unit spelling.
    return compact.replace(
        "Return(Bool(true)),))", "Return(Bool(true)),.Stmts))"
    )


def main() -> None:
    translated = (ROOT / "solution.mpy").read_text()
    spec = (ROOT / "spec.k").read_text()
    verification = (ROOT / "verification.k").read_text()

    submitted_module, _ = extract_call(translated, "Module")
    claim_module, _ = extract_call(spec, "Module")
    assert norm(submitted_module) == norm(claim_module)
    print("solution.mpy Module vs SPEC #loadAll Module=CONSTRUCTOR_IDENTICAL_AFTER_EMPTY_STMTS_UNIT_NORMALIZATION")

    submitted_function, _ = extract_call(submitted_module, "FuncDef")
    function_args = arguments(submitted_function)
    assert len(function_args) == 3
    assert norm(function_args[0]) == '"below_zero"'
    assert norm(function_args[1]) == 'Params("operations")'

    bridge_closure, _ = extract_call(verification, "closureVal")
    closure_args = arguments(bridge_closure)
    assert len(closure_args) == 4
    assert norm(closure_args[0]) == '"operations"'
    assert norm(closure_args[1]) == ".ParamNames"
    assert norm(closure_args[2]) == norm(function_args[2])
    assert norm(closure_args[3]) == "0"
    print("solution function binding/body vs VERIFICATION bridge closure=CONSTRUCTOR_IDENTICAL")

    spec_closure, _ = extract_call(spec, "closureVal")
    spec_closure_args = arguments(spec_closure)
    assert len(spec_closure_args) == 4
    assert norm(spec_closure_args[2]) == norm(function_args[2])
    print("solution function body vs SPEC destination closure=CONSTRUCTOR_IDENTICAL")

    normalized_spec = norm(spec)
    assert "~>Call(Name(\"below_zero\"),list(INPUT:ValSeq))=>belowFrom(0,INPUT)" in normalized_spec
    assert "requiresallInts(INPUT)" in normalized_spec
    print("SPEC call/result/precondition shape=PINNED_AND_RESULT_CONSTRAINING")


if __name__ == "__main__":
    main()
