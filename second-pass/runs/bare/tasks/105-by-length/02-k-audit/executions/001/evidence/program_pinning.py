#!/usr/bin/env python3
"""Structurally compare solution.mpy with verification.k's #solutionProgram."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import TypeAlias

Term: TypeAlias = str | int | tuple[str, tuple["Term", ...]]

TOKEN = re.compile(
    r'\s*(?:(?P<string>"(?:\\.|[^"\\])*")|(?P<int>-?\d+)'
    r"|(?P<identifier>[A-Za-z_#.][A-Za-z0-9_#.-]*)|(?P<punct>[(),]))"
)


def tokenize(source: str) -> list[str]:
    tokens: list[str] = []
    position = 0
    while position < len(source):
        match = TOKEN.match(source, position)
        if match is None:
            if source[position:].strip() == "":
                break
            raise SyntaxError(f"unrecognized text at offset {position}: {source[position:position+40]!r}")
        tokens.append(match.group(match.lastgroup or ""))
        position = match.end()
    return tokens


def parse(source: str) -> Term:
    tokens = tokenize(source)
    cursor = 0

    def parse_term() -> Term:
        nonlocal cursor
        if cursor >= len(tokens):
            raise SyntaxError("unexpected end of term")
        token = tokens[cursor]
        cursor += 1
        if token.startswith('"'):
            return json.loads(token)
        if re.fullmatch(r"-?\d+", token):
            return int(token)
        name = token
        if cursor < len(tokens) and tokens[cursor] == "(":
            cursor += 1
            arguments: list[Term] = []
            if cursor < len(tokens) and tokens[cursor] != ")":
                while True:
                    arguments.append(parse_term())
                    if cursor < len(tokens) and tokens[cursor] == ",":
                        cursor += 1
                        continue
                    break
            if cursor >= len(tokens) or tokens[cursor] != ")":
                raise SyntaxError(f"missing ')' for {name}")
            cursor += 1
            return (name, tuple(arguments))
        return name

    result = parse_term()
    if cursor != len(tokens):
        raise SyntaxError(f"unconsumed tokens: {tokens[cursor:]}")
    return result


mpy_path = Path("/tmp/audit-work/source/solution.mpy")
verification_path = Path("/tmp/audit-work/source/verification.k")
mpy_source = mpy_path.read_text(encoding="utf-8")
verification_source = verification_path.read_text(encoding="utf-8")

start_marker = "rule #solutionProgram =>"
end_marker = "\n\n  // A contract-level characterization"
start = verification_source.index(start_marker) + len(start_marker)
end = verification_source.index(end_marker, start)
proof_program_source = verification_source[start:end]

mpy_tree = parse(mpy_source)
proof_tree = parse(proof_program_source)
same = mpy_tree == proof_tree

print(f"translator_output={mpy_path}")
print(f"proof_constant_source={verification_path}")
print(f"translator_tree_sha256={hashlib.sha256(repr(mpy_tree).encode()).hexdigest()}")
print(f"proof_tree_sha256={hashlib.sha256(repr(proof_tree).encode()).hexdigest()}")
print(f"structurally_identical={same}")
if not same:
    print("translator_tree=" + repr(mpy_tree))
    print("proof_tree=" + repr(proof_tree))
raise SystemExit(0 if same else 1)
