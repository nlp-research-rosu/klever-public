#!/usr/bin/env python3
"""Check that the entry claim's closure contains the submitted MPY function body."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def call_contents(text: str, name: str, start: int = 0) -> tuple[str, int]:
    marker = name + "("
    begin = text.index(marker, start) + len(marker)
    depth = 1
    quoted = False
    escaped = False
    for index in range(begin, len(text)):
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
                return text[begin:index], index + 1
    raise ValueError(f"unclosed {name} call")


def split_top_level(text: str) -> list[str]:
    pieces: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(text):
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
            pieces.append(text[start:index].strip())
            start = index + 1
    pieces.append(text[start:].strip())
    return pieces


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SOLUTION_MPY SPEC_K")
        return 64
    solution_text = Path(sys.argv[1]).read_text()
    spec_text = Path(sys.argv[2]).read_text()

    function_text, _ = call_contents(solution_text, "FuncDef")
    function_args = split_top_level(function_text)
    submitted_while, _ = call_contents(function_args[2], "While")
    claimed_while, _ = call_contents(spec_text, "#while")
    closure_anchor = spec_text.index('"fibfib" |-> closureVal(')
    closure_text, _ = call_contents(spec_text, "closureVal", closure_anchor)
    closure_args = split_top_level(closure_text)

    checks = {
        "function_arity_is_3": len(function_args) == 3,
        "submitted_name_is_fibfib": function_args[0] == '"fibfib"',
        "submitted_params_are_n": compact(function_args[1]) == 'Params("n")',
        "claim_binding_is_fibfib": '"fibfib" |-> closureVal('
        in spec_text[closure_anchor : closure_anchor + 64],
        "claim_params_are_n": closure_args[0] == '"n"'
        and compact(closure_args[1]) == ".ParamNames",
        "claim_definition_environment_is_0": closure_args[3] == "0",
        "closure_body_byte_tokens_match_submitted_body": compact(closure_args[2])
        == compact(function_args[2]),
        "loop_claim_condition_and_body_match_submitted_while": compact(claimed_while)
        == compact(submitted_while),
    }
    for name, result in checks.items():
        print(f"{name}={str(result).lower()}")
    print(f"submitted_body_compact={compact(function_args[2])}")
    print(f"claimed_body_compact={compact(closure_args[2])}")
    print(f"submitted_while_compact={compact(submitted_while)}")
    print(f"claimed_while_compact={compact(claimed_while)}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
