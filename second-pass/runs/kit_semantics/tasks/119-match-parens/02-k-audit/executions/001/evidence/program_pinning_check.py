#!/usr/bin/env python3
"""Constructor-level comparison of translated function and claimed closure."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class Atom:
    kind: str
    value: object


@dataclasses.dataclass(frozen=True)
class Node:
    label: str
    arguments: tuple[object, ...]


@dataclasses.dataclass(frozen=True)
class Sequence:
    items: tuple[object, ...]


TOKEN = re.compile(
    r"""
    \s*(?:
        (?P<string>"(?:\\.|[^"\\])*")
      | (?P<int>-?[0-9]+)
      | (?P<ident>\.?[#A-Za-z][#A-Za-z0-9_-]*)
      | (?P<punct>[(),])
    )
    """,
    re.VERBOSE,
)


def balanced_call(text: str, start: int) -> str:
    open_paren = text.find("(", start)
    assert open_paren >= 0
    depth = 0
    in_string = False
    escaped = False
    for offset in range(open_paren, len(text)):
        character = text[offset]
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
                return text[start : offset + 1]
    raise AssertionError("unterminated call")


def tokenize(text: str):
    tokens = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        assert match, (position, text[position : position + 40])
        position = match.end()
        kind = match.lastgroup
        assert kind
        value = match.group(kind)
        tokens.append((kind, value))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position == len(self.tokens):
            return None
        return self.tokens[self.position]

    def consume(self, expected=None):
        token = self.peek()
        assert token is not None
        if expected is not None:
            assert token[1] == expected, (token, expected)
        self.position += 1
        return token

    def atom(self):
        kind, value = self.consume()
        if kind == "string":
            return Atom("string", json.loads(value))
        if kind == "int":
            return Atom("int", int(value))
        assert kind == "ident"
        if self.peek() and self.peek()[1] == "(":
            self.consume("(")
            arguments = []
            if self.peek() and self.peek()[1] == ")":
                self.consume(")")
                return Node(value, ())
            while True:
                items = []
                while self.peek() and self.peek()[1] not in {",", ")"}:
                    items.append(self.atom())
                arguments.append(
                    items[0] if len(items) == 1 else Sequence(tuple(items))
                )
                separator = self.consume()
                if separator[1] == ")":
                    break
                assert separator[1] == ","
                if self.peek() and self.peek()[1] == ")":
                    arguments.append(Sequence(()))
                    self.consume(")")
                    break
            return Node(value, tuple(arguments))
        return Atom("ident", value)

    def one(self):
        result = self.atom()
        assert self.position == len(self.tokens), self.tokens[self.position :]
        return result


def parse_call(text: str, label: str):
    start = text.index(label + "(")
    return Parser(tokenize(balanced_call(text, start))).one()


def normalize(term):
    if term == Atom("ident", ".Stmts"):
        return Sequence(())
    if isinstance(term, Node):
        return Node(term.label, tuple(normalize(item) for item in term.arguments))
    if isinstance(term, Sequence):
        normalized = []
        for item in term.items:
            value = normalize(item)
            if value != Sequence(()) or len(term.items) == 1:
                normalized.append(value)
        return Sequence(tuple(normalized))
    return term


def count_nodes(term) -> int:
    if isinstance(term, Node):
        return 1 + sum(count_nodes(item) for item in term.arguments)
    if isinstance(term, Sequence):
        return sum(count_nodes(item) for item in term.items)
    return 1


solution_text = Path(
    "/tmp/audit-work/119-match-parens/solution.regenerated.mpy"
).read_text()
spec_text = Path("/tmp/audit-work/119-match-parens/spec.k").read_text()

module = parse_call(solution_text, "Module")
assert isinstance(module, Node) and module.label == "Module"
assert len(module.arguments) == 1
function = module.arguments[0]
assert isinstance(function, Node) and function.label == "FuncDef"
assert function.arguments[0] == Atom("string", "match_parens")
assert function.arguments[1] == Node("Params", (Atom("string", "lst"),))

binding_match = re.search(
    r'"match_parens"\s*\|->\s*closureVal\(', spec_text
)
assert binding_match
closure_start = spec_text.index("closureVal(", binding_match.start())
closure = Parser(
    tokenize(balanced_call(spec_text, closure_start))
).one()
assert isinstance(closure, Node) and closure.label == "closureVal"
assert closure.arguments[0] == Atom("string", "lst")
assert closure.arguments[2] == Atom("int", 0)

translated_body = normalize(function.arguments[2])
claimed_body = normalize(closure.arguments[1])
assert translated_body == claimed_body

serialized = repr(translated_body).encode()
print('scope_binding: "match_parens" |-> closureVal')
print('parameter_binding: "lst" at parent scope 0')
print(f"normalized_constructor_nodes: {count_nodes(translated_body)}")
print(f"normalized_body_sha256: {hashlib.sha256(serialized).hexdigest()}")
print("allowed_normalization: explicit .Stmts versus empty Stmts argument only")
print("PROGRAM PINNING: PASS")
