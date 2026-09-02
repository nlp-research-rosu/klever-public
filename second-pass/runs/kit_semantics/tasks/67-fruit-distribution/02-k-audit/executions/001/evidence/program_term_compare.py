#!/usr/bin/env python3
"""Mechanical constructor-level comparison of translation and entry claim."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from pathlib import Path
from typing import Any


@dataclasses.dataclass(frozen=True)
class Node:
    head: str
    children: tuple[Any, ...]


TOKEN = re.compile(r'\s*(?:(?P<string>"(?:\\.|[^"\\])*")|(?P<int>-?[0-9]+)|(?P<id>[.#A-Za-z_][.#A-Za-z_0-9-]*)|(?P<punct>[(),]))')


class Parser:
    def __init__(self, text: str):
        self.tokens = [
            next(value for value in match.groupdict().values() if value is not None)
            for match in TOKEN.finditer(text)
        ]
        self.index = 0

    def peek(self) -> str | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self) -> str:
        token = self.peek()
        if token is None:
            raise ValueError("unexpected end")
        self.index += 1
        return token

    def term(self) -> Any:
        token = self.take()
        if token == "(":
            children = self.arguments(")")
            return Node("tuple", tuple(children))
        if token.startswith('"'):
            return json.loads(token)
        if re.fullmatch(r"-?[0-9]+", token):
            return int(token)
        if self.peek() == "(":
            self.take()
            return Node(token, tuple(self.arguments(")")))
        return token

    def arguments(self, end: str) -> list[Any]:
        children: list[Any] = []
        if self.peek() == end:
            self.take()
            return children
        while True:
            if self.peek() == ",":
                children.append(".OMITTED")
            else:
                children.append(self.term())
            if self.peek() == end:
                self.take()
                return children
            if self.take() != ",":
                raise ValueError("expected comma")
            if self.peek() == end:
                children.append(".OMITTED")
                self.take()
                return children


def balanced_constructor(text: str, head: str, start: int = 0) -> str:
    begin = text.index(head + "(", start)
    return balanced_group(text, begin)


def balanced_group(text: str, begin: int) -> str:
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
            if depth == 0:
                return text[begin : index + 1]
    raise ValueError("unbalanced constructor/group")


def parse_one(text: str) -> Any:
    parser = Parser(text)
    result = parser.term()
    if parser.peek() is not None:
        raise ValueError(f"unparsed token: {parser.peek()}")
    return result


def canonical(term: Any) -> Any:
    if not isinstance(term, Node):
        return term
    children = [canonical(child) for child in term.children]
    if term.head == "Call":
        callee = children[0]
        args = [
            child
            for child in children[1:]
            if child != ".Exprs" and child != ".OMITTED"
        ]
        return ["Call", callee, args]
    if term.head == "Params":
        return ["ParamNames", *children]
    if term.head == "tuple":
        return ["ParamNames", *children]
    return [term.head, *children]


translated_path = Path("/tmp/audit-work/fruit67/solution.regenerated.mpy")
spec_path = Path("/tmp/audit-work/fruit67/spec.k")
functions_path = Path("/tmp/audit-work/fruit67/reference-semantics/semantics/functions.k")
translated = translated_path.read_text()
spec = spec_path.read_text()
functions = functions_path.read_text()

assert 'FuncDef("fruit_distribution", Params("s", "n"),' in translated
assert re.search(
    r"FuncDef\(F:String, Params\(PNS:ParamNames\), BODY:Stmts\).*?"
    r"closureVal\(PNS, BODY, L\)",
    functions,
    re.S,
), "fixed FuncDef-to-closure mapping was not found"

translated_return = canonical(parse_one(balanced_constructor(translated, "Return")))
claim_return = canonical(parse_one(balanced_constructor(spec, "Return")))
translated_params = canonical(parse_one(balanced_constructor(translated, "Params")))
closure_index = spec.index("closureVal(")
claim_param_begin = spec.index("(", closure_index + len("closureVal("))
claim_param_text = balanced_group(spec, claim_param_begin)
claim_params = canonical(parse_one(claim_param_text))

assert translated_return == claim_return
assert translated_params == claim_params
assert re.search(r"closureVal\(.*?\.Stmts,\s*0\)", spec, re.S)

rendered = json.dumps(
    {
        "function_name": "fruit_distribution",
        "parameters": translated_params,
        "body": translated_return,
        "defining_environment": 0,
    },
    sort_keys=True,
    separators=(",", ":"),
)
print(f"TRANSLATED_RETURN={json.dumps(translated_return, separators=(',', ':'))}")
print(f"CLAIM_RETURN={json.dumps(claim_return, separators=(',', ':'))}")
print(f"TRANSLATED_PARAMS={json.dumps(translated_params, separators=(',', ':'))}")
print(f"CLAIM_PARAMS={json.dumps(claim_params, separators=(',', ':'))}")
print(f"NORMALIZED_CLOSURE_SHA256={hashlib.sha256(rendered.encode()).hexdigest()}")
print("PROGRAM_TERM_COMPARE=PASS")
