#!/usr/bin/env python3
"""Compare the submitted translated function body with proof syntax macros."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/31-is-prime")


@dataclass(frozen=True)
class Atom:
    value: str


@dataclass(frozen=True)
class Node:
    name: str
    args: tuple[tuple[object, ...], ...]


TOKEN = re.compile(
    r'\s*(?:(?P<string>"(?:\\.|[^"\\])*")|'
    r"(?P<name>[#.]?[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+)|"
    r"(?P<punct>[(),]))"
)


def tokenize(text: str) -> list[str]:
    tokens = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if match is None:
            if text[position:].strip() == "":
                break
            raise ValueError(f"unparsed text at {position}: {text[position:position + 40]!r}")
        tokens.append(match.group(match.lastgroup))
        position = match.end()
    return tokens


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = 0

    def peek(self) -> str | None:
        if self.position == len(self.tokens):
            return None
        return self.tokens[self.position]

    def take(self) -> str:
        token = self.peek()
        if token is None:
            raise ValueError("unexpected end of tokens")
        self.position += 1
        return token

    def value(self) -> object:
        token = self.take()
        if self.peek() != "(":
            return Atom(token)
        self.take()
        args: list[tuple[object, ...]] = []
        if self.peek() == ")":
            self.take()
            return Node(token, tuple(args))
        while True:
            values = []
            while self.peek() not in {",", ")", None}:
                values.append(self.value())
            args.append(tuple(values))
            delimiter = self.take()
            if delimiter == ")":
                break
        return Node(token, tuple(args))

    def sequence(self) -> tuple[object, ...]:
        values = []
        while self.peek() is not None:
            values.append(self.value())
        return tuple(values)


def parse(text: str) -> tuple[object, ...]:
    return Parser(tokenize(text)).sequence()


def macro_rhs(source: str, name: str) -> tuple[object, ...]:
    match = re.search(
        rf"(?ms)^\s*rule\s+{re.escape(name)}\s*\n\s*=>\s*(.*?)"
        rf"(?=^\s*(?://|(?:syntax|rule|endmodule)\b))",
        source,
    )
    if match is None:
        raise ValueError(f"missing macro rule {name}")
    return parse(match.group(1))


def expand(value: object, macros: dict[str, tuple[object, ...]]) -> tuple[object, ...]:
    if isinstance(value, Atom):
        return macros.get(value.value, (value,))
    if not isinstance(value, Node):
        raise TypeError(value)
    expanded_args = []
    for argument in value.args:
        expanded_argument = []
        for child in argument:
            expanded_argument.extend(expand(child, macros))
        expanded_args.append(tuple(expanded_argument))
    return (Node(value.name, tuple(expanded_args)),)


def normalize(value: object) -> object:
    """Treat K's explicit .Stmts unit as the translator's empty list argument."""
    if isinstance(value, Atom):
        return value
    if not isinstance(value, Node):
        raise TypeError(value)
    normalized_args = []
    for argument in value.args:
        normalized_args.append(
            tuple(
                normalize(child)
                for child in argument
                if not (isinstance(child, Atom) and child.value == ".Stmts")
            )
        )
    return Node(value.name, tuple(normalized_args))


def main() -> int:
    translated = parse((ROOT / "solution.mpy").read_text(encoding="utf-8"))
    if len(translated) != 1 or not isinstance(translated[0], Node):
        raise ValueError("unexpected translated module shape")
    module = translated[0]
    function = module.args[0][0]
    if not isinstance(function, Node) or function.name != "FuncDef":
        raise ValueError("expected one FuncDef")
    translated_body = function.args[2]

    verification = (ROOT / "verification.k").read_text(encoding="utf-8")
    macros = {
        "#primeCond": macro_rhs(verification, "#primeCond"),
        "#primeLoopBody": macro_rhs(verification, "#primeLoopBody"),
    }
    entry = macro_rhs(verification, "#entryBody")
    expanded_entry = []
    for item in entry:
        expanded_entry.extend(expand(item, macros))

    same_body = tuple(normalize(item) for item in expanded_entry) == tuple(
        normalize(item) for item in translated_body
    )
    while_nodes = [
        node
        for node in translated_body
        if isinstance(node, Node) and node.name == "While"
    ]
    if len(while_nodes) != 1:
        raise ValueError(f"expected one While, found {len(while_nodes)}")
    while_node = while_nodes[0]
    same_condition = tuple(
        normalize(child)
        for item in macros["#primeCond"]
        for child in expand(item, macros)
    ) == tuple(normalize(child) for child in while_node.args[0])
    same_loop_body = tuple(
        normalize(child)
        for item in macros["#primeLoopBody"]
        for child in expand(item, macros)
    ) == tuple(normalize(child) for child in while_node.args[1])

    spec = (ROOT / "spec.k").read_text(encoding="utf-8")
    print(f"entry_macro_equals_translated_function_body={same_body}")
    print(f"condition_macro_equals_translated_while_condition={same_condition}")
    print(f"loop_body_macro_equals_translated_while_body={same_loop_body}")
    print(f"spec_entry_body_occurrences={spec.count('#entryBody')}")
    print(f"spec_while_macro_occurrences={spec.count('#while(#primeCond, #primeLoopBody)')}")
    print("solution_mpy_is_required_by_k_source=false")
    return 0 if same_body and same_condition and same_loop_body else 1


if __name__ == "__main__":
    raise SystemExit(main())
