#!/usr/bin/env python3
"""Mechanically compare the translated module with the claimed K constructor term."""

from __future__ import annotations

import re
from pathlib import Path


Token = tuple[str, str]


def tokenize(text: str) -> list[Token]:
    pattern = re.compile(
        r"""
        (?P<space>\s+)
      | (?P<comment>//[^\n]*)
      | (?P<string>"(?:\\.|[^"\\])*")
      | (?P<number>-?[0-9]+)
      | (?P<ident>\.?[A-Za-z#][A-Za-z0-9#-]*)
      | (?P<punct>[(),])
        """,
        re.VERBOSE,
    )
    tokens: list[Token] = []
    position = 0
    while position < len(text):
        match = pattern.match(text, position)
        if not match:
            raise ValueError(f"unrecognized token at {position}: {text[position:position+40]!r}")
        position = match.end()
        if match.lastgroup not in {"space", "comment"}:
            tokens.append((match.lastgroup or "", match.group()))
    return tokens


def parse_term(tokens: list[Token], position: int = 0):
    kind, value = tokens[position]
    if kind not in {"ident", "string", "number"}:
        raise ValueError(f"expected atom at token {position}: {tokens[position]!r}")
    position += 1
    if position < len(tokens) and tokens[position][1] == "(":
        position += 1
        arguments = []
        if tokens[position][1] != ")":
            while True:
                argument, position = parse_term(tokens, position)
                arguments.append(argument)
                if tokens[position][1] == ",":
                    position += 1
                    continue
                break
        if tokens[position][1] != ")":
            raise ValueError(f"expected ')' at token {position}")
        position += 1
        return ("call", value, tuple(arguments)), position
    return ("atom", kind, value), position


def parse_complete(text: str):
    tokens = tokenize(text)
    term, position = parse_term(tokens)
    if position != len(tokens):
        raise ValueError(f"unconsumed tokens: {tokens[position:position+10]!r}")
    return term


def extract_rule_rhs(text: str, name: str) -> str:
    match = re.search(
        rf"(?ms)^\s*rule\s+{re.escape(name)}\s*=>\s*(.*?)"
        rf"(?=^\s*(?:syntax|rule|endmodule)\b)",
        text,
    )
    if not match:
        raise ValueError(f"could not extract rule {name}")
    return match.group(1).strip()


def expand(term, definitions):
    if term[0] == "atom":
        value = term[2]
        if value in definitions:
            return expand(definitions[value], definitions)
        return term
    _, name, arguments = term
    expanded_arguments = tuple(expand(argument, definitions) for argument in arguments)
    # The translator prints empty parameter-name collections as `CellVars()`
    # and `FreeVars()`; K's parsed constructor term spells the same empty
    # collection explicitly as `.ParamNames`.
    if name in {"CellVars", "FreeVars"} and not expanded_arguments:
        expanded_arguments = (("atom", "ident", ".ParamNames"),)
    return ("call", name, expanded_arguments)


solution_text = Path("/tmp/audit-work/reconstruction/solution.mpy").read_text()
verification_text = Path("/tmp/audit-work/reconstruction/verification.k").read_text()

definition_names = [
    "sortArrayLambda",
    "sortArrayBody",
    "sortArrayClosure",
    "sortArrayModule",
    "popcountKeyClosure",
]
definitions = {
    name: parse_complete(extract_rule_rhs(verification_text, name))
    for name in definition_names
}

translated_module = expand(parse_complete(solution_text), definitions)
claimed_module = expand(definitions["sortArrayModule"], definitions)

translated_body = translated_module[2][0][2][2]
claimed_body = expand(definitions["sortArrayBody"], definitions)

print(f"MODULE_CONSTRUCTOR_EQUAL {translated_module == claimed_module}")
print(f"FUNCTION_BODY_EQUAL {translated_body == claimed_body}")
print(f"TRANSLATED_MODULE {translated_module!r}")
print(f"CLAIMED_MODULE {claimed_module!r}")

if translated_module != claimed_module or translated_body != claimed_body:
    raise SystemExit(1)
