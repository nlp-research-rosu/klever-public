#!/usr/bin/env python3
"""Mechanical constructor-tree comparison and concrete claim witnesses."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(),]')


def tokenize(text: str) -> list[str]:
    tokens = TOKEN.findall(text)
    residue = TOKEN.sub("", text)
    assert residue.strip() == "", f"unparsed syntax: {residue!r}"
    return tokens


def parse_constructor(text: str):
    tokens = tokenize(text)
    position = 0

    def parse_one():
        nonlocal position
        token = tokens[position]
        position += 1
        if token.startswith('"'):
            return ("String", json.loads(token))
        if re.fullmatch(r"-?[0-9]+", token):
            return ("IntegerToken", int(token))
        identifier = token
        if position < len(tokens) and tokens[position] == "(":
            position += 1
            arguments = []
            if tokens[position] != ")":
                while True:
                    arguments.append(parse_one())
                    if tokens[position] == ",":
                        position += 1
                        continue
                    break
            assert tokens[position] == ")"
            position += 1
            return ("Constructor", identifier, tuple(arguments))
        return ("Atom", identifier)

    tree = parse_one()
    assert position == len(tokens), tokens[position:]
    return tree


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


submitted = Path("/candidate/solution.mpy").read_text()
regenerated = Path(
    "/tmp/audit-work/generated-tests/solution-regenerated.mpy"
).read_text()
spec_text = Path("/candidate/spec.k").read_text()
claim_program = spec_text.split("<k>", 1)[1].split("=> .K", 1)[0]

submitted_tree = parse_constructor(submitted)
regenerated_tree = parse_constructor(regenerated)
claim_tree = parse_constructor(claim_program)
assert submitted_tree == regenerated_tree == claim_tree

assert claim_tree[0:2] == ("Constructor", "Module")
function = claim_tree[2][0]
assert function[0:2] == ("Constructor", "FuncDef")
assert function[2][0] == ("String", "get_max_triples")

candidate = load_entry("pin_candidate", Path("/candidate/solution.py"))
canonical = load_entry("pin_canonical", Path("/reference/canonical.py"))


def claimed_result(n: int) -> int:
    class_zero = (n + 1) // 3
    class_one = n - class_zero

    def choose3(x: int) -> int:
        return x * (x - 1) * (x - 2) // 6

    return choose3(class_zero) + choose3(class_one)


witnesses = [1, 5, 10, 100]
for n in witnesses:
    assert n >= 1
    expected = claimed_result(n)
    actual_candidate = candidate(n)
    actual_canonical = canonical(n)
    print(
        f"SATISFYING WITNESS N={n}: precondition={n >= 1}; "
        f"claim_result={expected}; candidate={actual_candidate}; "
        f"canonical={actual_canonical}"
    )
    assert expected == actual_candidate == actual_canonical

print(
    "EXHIBITED ENTRY STATE: exact claim program in <k>, <input> 5 </input>, "
    "<env> .Map </env>, <result> noResult </result>; requires 5 >=Int 1"
)
print("submitted/regenerated/claim constructor trees: IDENTICAL")
print("PROGRAM PINNING AND SATISFIABILITY: PASS")
