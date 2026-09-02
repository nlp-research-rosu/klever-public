#!/usr/bin/env python3
"""Extract the balanced Module(...) term nested in the entry claim's #loadAll."""

from __future__ import annotations

import argparse
from pathlib import Path


def balanced_call(text: str, start: int) -> str:
    open_paren = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
                return text[start : index + 1]
    raise ValueError("unbalanced constructor call")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--rule-output", type=Path)
    args = parser.parse_args()

    text = args.spec.read_text()
    load_marker = "#loadAll("
    positions = []
    offset = 0
    while True:
        position = text.find(load_marker, offset)
        if position < 0:
            break
        positions.append(position)
        offset = position + len(load_marker)
    if len(positions) != 1:
        raise ValueError(f"expected one #loadAll entry term, found {len(positions)}")

    module_start = text.find("Module(", positions[0] + len(load_marker))
    if module_start < 0:
        raise ValueError("entry #loadAll does not contain Module(...)")
    module = balanced_call(text, module_start)
    args.output.write_text(module + "\n")
    if args.rule_output is not None:
        args.rule_output.write_text(
            f"<k> #loadAll({module}) => #loadAll({module}) </k>\n"
        )
    print(f"entry #loadAll count: {len(positions)}")
    print(f"extracted bytes: {len((module + chr(10)).encode())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
