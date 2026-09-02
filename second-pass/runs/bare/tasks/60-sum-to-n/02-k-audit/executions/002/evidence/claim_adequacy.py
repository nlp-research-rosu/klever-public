#!/usr/bin/env python3
"""Mechanical constructor comparison and concrete claim witnesses."""

from __future__ import annotations

import importlib.util
import re
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/reconstruction")
CANDIDATE = ROOT / "candidate"


@dataclass(frozen=True)
class Node:
    constructor: str
    arguments: tuple[object, ...]


TOKEN = re.compile(
    r'\s*(?:(?P<string>"(?:[^"\\]|\\.)*")|(?P<int>-?[0-9]+)|'
    r"(?P<identifier>[A-Za-z_][A-Za-z_0-9]*)(?P<punct>[(),])?|(?P<onlypunct>[(),]))"
)


class Parser:
    def __init__(self, text: str):
        self.tokens: list[tuple[str, str]] = []
        position = 0
        while position < len(text):
            match = TOKEN.match(text, position)
            if match is None:
                if text[position:].strip() == "":
                    break
                raise ValueError(f"unparsed input at {position}: {text[position:position+40]!r}")
            position = match.end()
            if match.group("string") is not None:
                self.tokens.append(("string", match.group("string")))
            elif match.group("int") is not None:
                self.tokens.append(("int", match.group("int")))
            elif match.group("identifier") is not None:
                self.tokens.append(("identifier", match.group("identifier")))
                if match.group("punct") is not None:
                    self.tokens.append(("punct", match.group("punct")))
            else:
                self.tokens.append(("punct", match.group("onlypunct")))
        self.index = 0

    def peek(self) -> tuple[str, str] | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self, kind: str, value: str | None = None) -> str:
        token = self.peek()
        if token is None or token[0] != kind or (value is not None and token[1] != value):
            raise ValueError(f"expected {(kind, value)}, got {token}")
        self.index += 1
        return token[1]

    def parse_value(self) -> object:
        token = self.peek()
        if token is None:
            raise ValueError("unexpected end")
        if token[0] == "string":
            raw = self.take("string")
            return bytes(raw[1:-1], "utf-8").decode("unicode_escape")
        if token[0] == "int":
            return int(self.take("int"))
        name = self.take("identifier")
        self.take("punct", "(")
        arguments: list[object] = []
        if self.peek() != ("punct", ")"):
            while True:
                arguments.append(self.parse_value())
                if self.peek() != ("punct", ","):
                    break
                self.take("punct", ",")
        self.take("punct", ")")
        return Node(name, tuple(arguments))

    def parse(self) -> Node:
        result = self.parse_value()
        if not isinstance(result, Node):
            raise ValueError("top level is not a constructor")
        if self.peek() is not None:
            raise ValueError(f"trailing token {self.peek()}")
        return result


def extract_balanced_module(specification: str) -> str:
    k_start = specification.index("<k>")
    start = specification.index("Module(", k_start)
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(specification)):
        character = specification[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return specification[start : index + 1]
    raise ValueError("unbalanced Module term")


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


submitted_text = (CANDIDATE / "solution.mpy").read_text()
spec_text = (CANDIDATE / "spec.k").read_text()
claimed_text = extract_balanced_module(spec_text)
submitted_tree = Parser(submitted_text).parse()
claimed_tree = Parser(claimed_text).parse()

print(f"submitted_constructor_tree={submitted_tree}")
print(f"claimed_constructor_tree={claimed_tree}")
print(f"constructor_tree_equal={submitted_tree == claimed_tree}")
assert submitted_tree == claimed_tree

function = submitted_tree.arguments[0]
assert isinstance(function, Node) and function.constructor == "FuncDef"
function_name, parameters, body = function.arguments
print(f"function_binding={function_name!r}")
print(f"parameters={parameters}")
print(f"body={body}")
assert function_name == "sum_to_n"
assert parameters == Node("Params", ("n",))

canonical = load_module("trusted_canonical_claim", ROOT / "trusted/canonical.py")
candidate = load_module("candidate_subject_claim", CANDIDATE / "solution.py")
print("formal_precondition=N >=Int 0")
print("formal_postcondition=result == sumSpec(N) == (N * (N + 1)) /Int 2")
for n in [0, 1, 2, 30, 100]:
    assert n >= 0
    claimed_result = n * (n + 1) // 2
    candidate_result = candidate.sum_to_n(n)
    canonical_result = canonical.sum_to_n(n)
    print(
        f"SATISFYING_WITNESS N={n} precondition=True "
        f"claimed={claimed_result} candidate={candidate_result} canonical={canonical_result}"
    )
    assert claimed_result == candidate_result == canonical_result

n = -2
print(
    f"EXCLUDED_WITNESS N={n} precondition={n >= 0} "
    f"candidate={candidate.sum_to_n(n)} canonical={canonical.sum_to_n(n)}"
)
print("CLAIM_ADEQUACY_CHECK: PASS_FOR_RESTRICTED_DOMAIN")
