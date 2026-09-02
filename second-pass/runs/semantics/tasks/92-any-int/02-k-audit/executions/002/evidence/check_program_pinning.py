#!/usr/bin/env python3
"""Mechanical comparison of submitted MPY function body to the proof body macro."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


SCRATCH = Path("/tmp/audit-work/92-any-int")


@dataclass(frozen=True)
class Node:
    name: str
    args: tuple[object, ...]


TOKEN = re.compile(
    r'\s*(?:(?P<string>"(?:\\.|[^"\\])*")|'
    r"(?P<ident>[A-Za-z_][A-Za-z0-9_-]*)|"
    r"(?P<number>-?[0-9]+)|(?P<punct>[(),]))"
)


class Parser:
    def __init__(self, text: str):
        self.tokens: list[tuple[str, str]] = []
        position = 0
        while position < len(text):
            match = TOKEN.match(text, position)
            if not match:
                if text[position:].strip() == "":
                    position = len(text)
                    break
                raise ValueError(f"unparsed input at {text[position:position+80]!r}")
            kind = next(name for name, value in match.groupdict().items() if value)
            self.tokens.append((kind, match.group(kind)))
            position = match.end()
        self.index = 0

    def peek(self, value: str | None = None) -> bool:
        if self.index >= len(self.tokens):
            return False
        return value is None or self.tokens[self.index][1] == value

    def pop(self, value: str | None = None) -> tuple[str, str]:
        if not self.peek(value):
            got = self.tokens[self.index] if self.index < len(self.tokens) else None
            raise ValueError(f"expected {value!r}, got {got!r}")
        token = self.tokens[self.index]
        self.index += 1
        return token

    def term(self) -> object:
        kind, value = self.pop()
        if kind == "string":
            return json.loads(value)
        if kind == "number":
            return int(value)
        if kind != "ident":
            raise ValueError(f"unexpected token {(kind, value)!r}")
        if not self.peek("("):
            return value
        self.pop("(")
        args: list[object] = []
        if not self.peek(")"):
            while True:
                args.append(self.term())
                if self.peek(","):
                    self.pop(",")
                    continue
                break
        self.pop(")")
        return Node(value, tuple(args))

    def all(self) -> object:
        result = self.term()
        if self.index != len(self.tokens):
            raise ValueError(f"trailing tokens: {self.tokens[self.index:]}")
        return result


def balanced_term_after(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    start += len(text[start:]) - len(text[start:].lstrip())
    open_pos = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for position in range(open_pos, len(text)):
        char = text[position]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : position + 1]
    raise ValueError("unbalanced term")


submitted = Parser((SCRATCH / "solution.submitted.mpy").read_text()).all()
if not isinstance(submitted, Node) or submitted.name != "Module":
    raise AssertionError(f"expected Module, got {submitted!r}")
if len(submitted.args) != 1:
    raise AssertionError(f"expected one module statement, got {len(submitted.args)}")
function = submitted.args[0]
if not isinstance(function, Node) or function.name != "FuncDef":
    raise AssertionError(f"expected FuncDef, got {function!r}")
name, params, body = function.args

verification_text = (SCRATCH / "verification.k").read_text()
macro_text = balanced_term_after(verification_text, "rule anyIntBody\n    =>")
macro_body = Parser(macro_text).all()

expected_params = Node("Params", ("x", "y", "z"))
binding_pattern = re.compile(
    r'toCall\s*\(\s*closureVal\s*\(\s*'
    r'\(\s*"x"\s*,\s*"y"\s*,\s*"z"\s*\)\s*,\s*'
    r'anyIntBody\s*,\s*0\s*\)\s*\)',
    re.MULTILINE,
)

print(f"SUBMITTED_FUNCTION_NAME={name!r}")
print(f"PARAMETERS_MATCH={params == expected_params}")
print(f"BODY_CONSTRUCTOR_MATCH={body == macro_body}")
print(f"EXACT_CLOSURE_HARNESS_MATCH={bool(binding_pattern.search(verification_text))}")
print(f"SUBMITTED_BODY={body!r}")
print(f"PROOF_MACRO_BODY={macro_body!r}")

ok = (
    name == "any_int"
    and params == expected_params
    and body == macro_body
    and bool(binding_pattern.search(verification_text))
)
print(f"PROGRAM_PINNING_CHECK={ok}")
sys.exit(0 if ok else 1)
