#!/usr/bin/env python3
"""Mechanical constructor-tree comparison of solution.mpy and both claim programs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import TypeAlias


Tree: TypeAlias = tuple[str, tuple["Tree | str | int", ...]]


TOKEN = re.compile(
    r"""\s*(?:
        (?P<string>"(?:\\.|[^"\\])*")
      | (?P<int>-?[0-9]+)
      | (?P<name>[A-Za-z_][A-Za-z0-9_-]*)
      | (?P<punct>[(),])
    )""",
    re.VERBOSE,
)


def tokens(text: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if match is None:
            if text[position:].strip() == "":
                break
            raise ValueError(f"unparsed text at {position}: {text[position:position+40]!r}")
        position = match.end()
        kind = match.lastgroup
        assert kind is not None
        result.append((kind, match.group(kind)))
    return result


def parse_constructor(text: str) -> Tree:
    stream = tokens(text)
    index = 0

    def parse_atom() -> Tree | str | int:
        nonlocal index
        kind, value = stream[index]
        index += 1
        if kind == "string":
            return json.loads(value)
        if kind == "int":
            return int(value)
        if kind != "name":
            raise ValueError(f"expected atom, got {(kind, value)}")
        name = value
        if index >= len(stream) or stream[index] != ("punct", "("):
            return name
        index += 1
        arguments: list[Tree | str | int] = []
        if stream[index] != ("punct", ")"):
            while True:
                arguments.append(parse_atom())
                if stream[index] == ("punct", ","):
                    index += 1
                    continue
                break
        if stream[index] != ("punct", ")"):
            raise ValueError(f"expected close paren, got {stream[index]}")
        index += 1
        return (name, tuple(arguments))

    tree = parse_atom()
    if index != len(stream) or not isinstance(tree, tuple):
        raise ValueError("constructor parse did not consume one tree")
    return tree


def first_argument(text: str, call_name: str, start: int = 0) -> str:
    marker = call_name + "("
    call = text.index(marker, start)
    begin = call + len(marker)
    depth = 0
    in_string = False
    escaped = False
    for index in range(begin, len(text)):
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
        elif character == "," and depth == 0:
            return text[begin:index]
    raise ValueError(f"cannot extract first argument of {call_name}")


def stable_tree(tree: Tree) -> str:
    return repr(tree)


def main() -> None:
    solution_text = Path(
        "/tmp/audit-work/candidate/solution.regenerated.mpy"
    ).read_text(encoding="utf-8")
    spec_text = Path("/tmp/audit-work/candidate/spec.k").read_text(encoding="utf-8")
    source_tree = parse_constructor(solution_text)
    entry_tree = parse_constructor(first_argument(spec_text, "apply"))
    example_tree = parse_constructor(first_argument(spec_text, "run"))

    for label, tree in (
        ("regenerated", source_tree),
        ("entry-claim", entry_tree),
        ("example-claim", example_tree),
    ):
        serialized = stable_tree(tree).encode()
        print(
            f"TREE {label} sha256={hashlib.sha256(serialized).hexdigest()} "
            f"value={tree!r}"
        )
    print(f"ENTRY_PROGRAM_TREE_IDENTICAL {entry_tree == source_tree}")
    print(f"EXAMPLE_PROGRAM_TREE_IDENTICAL {example_tree == source_tree}")
    if entry_tree != source_tree or example_tree != source_tree:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
