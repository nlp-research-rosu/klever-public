#!/usr/bin/env python3
"""Extract and reconstruct the program terms actually used by verification.k."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def balanced_call(text: str, start: int) -> str:
    open_paren = text.find("(", start)
    if open_paren < 0:
        raise ValueError("missing opening parenthesis")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start : index + 1]
    raise ValueError("unterminated constructor")


def split_arguments(call: str) -> list[str]:
    inner = call[call.find("(") + 1 : -1]
    arguments: list[str] = []
    depth = 0
    start = 0
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
        elif character in "([{":
            depth += 1
        elif character in ")]}":
            depth -= 1
        elif character == "," and depth == 0:
            arguments.append(inner[start:index].strip())
            start = index + 1
    arguments.append(inner[start:].strip())
    return arguments


def write_module(path: Path, function: str) -> None:
    # In K rule bubbles, empty lists may be written with their unit `.Exprs`.
    # The external MPY program grammar spells the same unit as an empty
    # argument position, as emitted by the trusted translator.
    program_syntax = function.replace(".Exprs", "")
    path.write_text(f"Module(\n  {program_syntax})\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("verification", type=Path)
    parser.add_argument("load_out", type=Path)
    parser.add_argument("call_out", type=Path)
    args = parser.parse_args()
    text = args.verification.read_text(encoding="utf-8")

    load_rule = text.index("rule #loadCountDistinct")
    load_start = text.index("FuncDef(", load_rule)
    load_function = balanced_call(text, load_start)
    load_args = split_arguments(load_function)
    if len(load_args) != 3:
        raise ValueError(f"unexpected FuncDef arity: {len(load_args)}")
    write_module(args.load_out, load_function)

    call_rule = text.index("rule #callCountDistinct")
    closure_start = text.index("closureVal(", call_rule)
    closure = balanced_call(text, closure_start)
    closure_args = split_arguments(closure)
    if len(closure_args) != 3:
        raise ValueError(f"unexpected closureVal arity: {len(closure_args)}")
    if closure_args[2] != "0":
        raise ValueError(f"unexpected defining scope: {closure_args[2]}")

    param_seq = closure_args[0]
    if not (param_seq.startswith("(") and param_seq.endswith(")")):
        raise ValueError("unexpected closure parameter syntax")
    param_tokens = split_arguments(f"Params{param_seq}")
    if not param_tokens or param_tokens[-1] != ".ParamNames":
        raise ValueError("closure parameter list has no .ParamNames terminator")
    params = f"Params({', '.join(param_tokens[:-1])})"

    body = re.sub(r"\s*\.Stmts\s*$", "", closure_args[1])
    call_function = f"FuncDef({load_args[0]}, {params}, {body})"
    write_module(args.call_out, call_function)

    print(f"LOAD_FUNCTION_CHARS: {len(load_function)}")
    print(f"CALL_CLOSURE_CHARS: {len(closure)}")
    print(f"CALL_DEFINING_SCOPE: {closure_args[2]}")
    print("PINNED_PROGRAM_EXTRACTION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
