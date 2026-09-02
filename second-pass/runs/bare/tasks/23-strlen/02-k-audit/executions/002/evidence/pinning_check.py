#!/usr/bin/env python3
"""Mechanical constructor-tree comparison of solution.mpy and spec.k."""

from __future__ import annotations

import re
from pathlib import Path


TOKEN = re.compile(
    r'\s*(?:(?P<name>[A-Za-z][A-Za-z0-9]*)|'
    r'(?P<string>"(?:[^"\\]|\\.)*")|(?P<lpar>\()|'
    r'(?P<rpar>\))|(?P<comma>,))'
)


def module_slice(text: str) -> str:
    start = text.index("Module(")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
    raise AssertionError("unterminated Module constructor")


def parse(text: str):
    tokens: list[tuple[str, str]] = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if not match:
            raise AssertionError(f"unexpected constructor text at {position}")
        kind = next(key for key, value in match.groupdict().items() if value)
        tokens.append((kind, match.group(kind)))
        position = match.end()
    cursor = 0

    def term():
        nonlocal cursor
        kind, value = tokens[cursor]
        cursor += 1
        if kind == "string":
            return ("String", value)
        assert kind == "name", (kind, value)
        constructor = value
        assert tokens[cursor][0] == "lpar"
        cursor += 1
        arguments = []
        if tokens[cursor][0] != "rpar":
            while True:
                arguments.append(term())
                if tokens[cursor][0] == "comma":
                    cursor += 1
                    continue
                break
        assert tokens[cursor][0] == "rpar"
        cursor += 1
        return (constructor, tuple(arguments))

    result = term()
    assert cursor == len(tokens)
    return result


def main() -> None:
    mpy = Path(
        "/tmp/audit-work/23-strlen.30KKVy/work/solution.mpy"
    ).read_text()
    spec = Path(
        "/tmp/audit-work/23-strlen.30KKVy/work/spec.k"
    ).read_text()
    mpy_tree = parse(module_slice(mpy))
    claim_tree = parse(module_slice(spec))
    print(f"translated_tree={mpy_tree!r}")
    print(f"claim_tree={claim_tree!r}")
    print(f"constructor_tree_equal={mpy_tree == claim_tree}")
    raise SystemExit(0 if mpy_tree == claim_tree else 1)


if __name__ == "__main__":
    main()
