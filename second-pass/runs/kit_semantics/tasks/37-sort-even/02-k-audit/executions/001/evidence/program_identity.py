#!/usr/bin/env python3
"""Mechanical constructor-level identity check for the claimed MPY function body."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/37-sort-even")


def strip_k_whitespace(text: str) -> str:
    """Remove whitespace outside quoted strings."""
    result: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    if quoted:
        raise AssertionError("unterminated quoted string")
    return "".join(result)


def extract_balanced_call(text: str, start: int) -> str:
    open_paren = text.find("(", start)
    if open_paren < 0:
        raise AssertionError("call has no opening parenthesis")
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
    raise AssertionError("unbalanced constructor call")


def split_top_level_arguments(call: str) -> list[str]:
    open_paren = call.find("(")
    if open_paren < 0 or not call.endswith(")"):
        raise AssertionError("not a constructor call")
    content = call[open_paren + 1 : -1]
    arguments: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(content):
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
            arguments.append(content[start:index])
            start = index + 1
    arguments.append(content[start:])
    return arguments


def macro_rhs(text: str, name: str, next_rule: str) -> str:
    marker = f"rule {name}"
    start = text.index(marker)
    arrow = text.index("=>", start) + 2
    end = text.index(f"rule {next_rule}", arrow)
    return text[arrow:end].strip()


def main() -> None:
    submitted = (ROOT / "solution.mpy").read_text()
    regenerated = (ROOT / "regenerated-solution.mpy").read_text()
    verification = (ROOT / "verification.k").read_text()
    assert submitted == regenerated, "trusted regeneration is not byte-identical"

    function_start = submitted.index('FuncDef("sort_even"')
    function_call = extract_balanced_call(submitted, function_start)
    arguments = split_top_level_arguments(function_call)
    assert len(arguments) == 3, f"unexpected FuncDef arity: {len(arguments)}"
    assert strip_k_whitespace(arguments[0]) == '"sort_even"'
    assert strip_k_whitespace(arguments[1]) == 'Params("l")'
    translated_body = arguments[2]

    loop_rhs = macro_rhs(verification, "sortEvenLoopBody", "sortEvenBody")
    body_marker = "rule sortEvenBody"
    body_start = verification.index(body_marker)
    body_arrow = verification.index("=>", body_start) + 2
    body_end = verification.index("rule evenCount", body_arrow)
    body_rhs = verification[body_arrow:body_end].strip()
    expanded_body_rhs = body_rhs.replace("sortEvenLoopBody", loop_rhs)

    normalized_translated = strip_k_whitespace(translated_body)
    normalized_claimed = strip_k_whitespace(expanded_body_rhs)
    print(f"TRANSLATED BODY NORMALIZED LENGTH {len(normalized_translated)}")
    print(f"CLAIMED EXPANDED BODY NORMALIZED LENGTH {len(normalized_claimed)}")
    if normalized_translated != normalized_claimed:
        mismatch = next(
            (
                index
                for index, pair in enumerate(
                    zip(normalized_translated, normalized_claimed)
                )
                if pair[0] != pair[1]
            ),
            min(len(normalized_translated), len(normalized_claimed)),
        )
        print(f"FIRST MISMATCH OFFSET {mismatch}")
        print(
            "TRANSLATED CONTEXT "
            + normalized_translated[max(0, mismatch - 80) : mismatch + 80]
        )
        print(
            "CLAIMED CONTEXT "
            + normalized_claimed[max(0, mismatch - 80) : mismatch + 80]
        )
        raise AssertionError("claim macro body differs from translated function body")
    print("TRUSTED REGENERATION BYTE IDENTITY true")
    print("FUNCTION NAME IDENTITY true")
    print("PARAMETER CONSTRUCTOR IDENTITY true")
    print("EXPANDED FUNCTION BODY CONSTRUCTOR IDENTITY true")


if __name__ == "__main__":
    main()
