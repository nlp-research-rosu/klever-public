#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and SPEC's closure."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Node:
    name: str
    arguments: tuple[object, ...]


@dataclass(frozen=True)
class TupleTerm:
    items: tuple[object, ...]


class Parser:
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def whitespace(self) -> None:
        while self.position < len(self.text) and self.text[self.position].isspace():
            self.position += 1

    def parse(self):
        value = self.value()
        self.whitespace()
        if self.position != len(self.text):
            raise ValueError(f"unparsed suffix at {self.position}: {self.text[self.position:self.position+40]!r}")
        return value

    def value(self):
        self.whitespace()
        if self.position >= len(self.text):
            raise ValueError("unexpected end of input")
        current = self.text[self.position]
        if current == '"':
            return self.string()
        if current == "(":
            return self.tuple_term()
        if current == "-" or current.isdigit():
            return self.integer()
        name = self.identifier()
        self.whitespace()
        if self.position < len(self.text) and self.text[self.position] == "(":
            self.position += 1
            arguments = self.arguments(")")
            return Node(name, arguments)
        return Node(name, ())

    def string(self) -> str:
        start = self.position
        self.position += 1
        escaped = False
        while self.position < len(self.text):
            char = self.text[self.position]
            self.position += 1
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                import json

                return json.loads(self.text[start:self.position])
        raise ValueError("unterminated string")

    def integer(self) -> int:
        match = re.match(r"-?[0-9]+", self.text[self.position :])
        if match is None:
            raise ValueError(f"expected integer at {self.position}")
        self.position += len(match.group(0))
        return int(match.group(0))

    def identifier(self) -> str:
        match = re.match(r"[A-Za-z_.][A-Za-z0-9_.-]*", self.text[self.position :])
        if match is None:
            raise ValueError(f"expected identifier at {self.position}")
        self.position += len(match.group(0))
        return match.group(0)

    def tuple_term(self) -> TupleTerm:
        self.position += 1
        return TupleTerm(self.arguments(")"))

    def arguments(self, terminator: str) -> tuple[object, ...]:
        values = []
        self.whitespace()
        if self.position < len(self.text) and self.text[self.position] == terminator:
            self.position += 1
            return ()
        while True:
            values.append(self.value())
            self.whitespace()
            if self.position >= len(self.text):
                raise ValueError("unterminated arguments")
            current = self.text[self.position]
            self.position += 1
            if current == terminator:
                return tuple(values)
            if current != ",":
                raise ValueError(f"expected comma at {self.position - 1}")


def balanced_constructor(text: str, name: str) -> str:
    start = text.index(name + "(")
    position = start + len(name)
    depth = 0
    in_string = False
    escaped = False
    while position < len(text):
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
        position += 1
    raise ValueError(f"unterminated {name}")


def main() -> int:
    solution_text = Path("/tmp/audit-work/reconstruction/solution.regenerated.mpy").read_text()
    spec_text = Path("/tmp/audit-work/reconstruction/spec.k").read_text()

    module = Parser(solution_text).parse()
    assert isinstance(module, Node) and module.name == "Module"
    assert len(module.arguments) == 1
    function = module.arguments[0]
    assert isinstance(function, Node) and function.name == "FuncDef"
    assert len(function.arguments) == 3
    function_name, parameters, source_body = function.arguments
    assert function_name == "multiply"
    assert parameters == Node("Params", ("a", "b"))

    closure_text = balanced_constructor(spec_text, "closureVal")
    closure = Parser(closure_text).parse()
    assert closure == Node(
        "closureVal",
        (TupleTerm(("a", "b")), source_body, 0),
    )
    assert re.search(r'"multiply"\s*\|->\s*closureVal\s*\(', spec_text)
    assert re.search(
        r'Call\s*\(\s*Name\s*\(\s*"multiply"\s*\)\s*,\s*'
        r'Int\s*\(\s*A:Int\s*\)\s*,\s*Int\s*\(\s*B:Int\s*\)\s*\)',
        spec_text,
    )
    assert re.search(
        r'=>\s*pyMod\s*\(\s*A\s*,\s*10\s*\)\s*'
        r'\*Int\s*pyMod\s*\(\s*B\s*,\s*10\s*\)',
        spec_text,
    )
    assert "requires" not in "\n".join(spec_text.splitlines()[5:])

    print("trusted_regeneration_parsed=Module(FuncDef(...))")
    print("function_binding=multiply")
    print("parameter_names=(a,b)")
    print(f"body={source_body!r}")
    print("spec_closure_body_equals_regenerated_body=True")
    print("spec_call_targets_multiply_with_symbolic_Int_arguments=True")
    print("entry_requires_clause=absent")
    print("postcondition=pyMod(A,10) *Int pyMod(B,10)")
    print("PROGRAM_PINNING=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
