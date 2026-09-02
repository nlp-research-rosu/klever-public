#!/usr/bin/env python3
"""Extract the translated FuncDef body and emit constructor-level pinning claims."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced constructor term")


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate_pinning_spec.py SOLUTION_MPY")
    text = Path(sys.argv[1]).read_text()
    match = re.search(r"\bFuncDef\s*\(", text)
    if not match:
        raise ValueError("no FuncDef in translated module")
    open_index = text.index("(", match.start())
    close_index = matching_paren(text, open_index)
    args = split_top_level(text[open_index + 1 : close_index])
    if len(args) != 3 or args[0] != '"sort_array"':
        raise ValueError(f"unexpected entry FuncDef arguments: {args[:2]}")
    params_match = re.fullmatch(
        r"Params\s*\(\s*(\"(?:[^\"\\\\]|\\\\.)*\")\s*,\s*\.ParamNames\s*\)",
        args[1],
        re.S,
    )
    if not params_match:
        raise ValueError(f"unexpected params: {args[1]}")
    param = params_match.group(1)
    body = args[2]

    print('requires "verification.k"')
    print()
    print("module PINNING")
    print("  imports VERIFICATION")
    print()
    print("  claim <k> sortArrayBody =>")
    print(body)
    print("    ... </k>")
    print()
    print("  claim <k> sortArrayClosure =>")
    print(f"    closureVal(({param}, .ParamNames),")
    print(body)
    print("      , 0) ... </k>")
    print("endmodule")


if __name__ == "__main__":
    main()
