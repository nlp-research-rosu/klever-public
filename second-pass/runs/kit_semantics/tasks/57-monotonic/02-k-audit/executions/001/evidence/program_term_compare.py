#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and SPEC's body."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


TOKEN = re.compile(
    r"""
    \s*
    (
        "(?:\\.|[^"\\])*"
      | -?[0-9]+
      | [A-Za-z_#$][A-Za-z0-9_#$.\-]*(?::[A-Za-z_][A-Za-z0-9_]*)?
      | [(),]
    )
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Node:
    head: str
    args: tuple["Node", ...] = ()

    def serializable(self):
        return [self.head, *[arg.serializable() for arg in self.args]]


def lex(text: str) -> list[str]:
    return [match.group(1) for match in TOKEN.finditer(text)]


def parse_node(tokens: list[str], start: int) -> tuple[Node, int]:
    head = tokens[start]
    index = start + 1
    args: list[Node] = []
    if index < len(tokens) and tokens[index] == "(":
        index += 1
        while tokens[index] != ")":
            arg, index = parse_node(tokens, index)
            args.append(arg)
            if tokens[index] == ",":
                index += 1
            elif tokens[index] != ")":
                raise ValueError(
                    f"expected comma or close after {arg}, got {tokens[index]!r}"
                )
        index += 1
    return Node(head, tuple(args)), index


def extract(text: str, constructor: str, occurrence: int = 0) -> Node:
    tokens = lex(text)
    indices = [index for index, token in enumerate(tokens) if token == constructor]
    if occurrence >= len(indices):
        raise ValueError(f"{constructor} occurrence {occurrence} not found")
    node, _ = parse_node(tokens, indices[occurrence])
    return node


def digest(node: Node) -> str:
    encoded = json.dumps(node.serializable(), separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    solution_text = Path("/candidate/solution.mpy").read_text()
    spec_text = Path("/candidate/spec.k").read_text()
    solution_function = extract(solution_text, "FuncDef")
    claim_function = extract(spec_text, "FuncDef")
    claim_assignment = extract(spec_text, "Assign")

    print("solution_func_digest", digest(solution_function))
    print("claim_func_digest", digest(claim_function))
    print("function_constructor_identity", solution_function == claim_function)
    print(
        "claim_assignment",
        json.dumps(claim_assignment.serializable(), separators=(",", ":")),
    )

    expected_assignment = Node(
        "Assign",
        (
            Node("Name", (Node('"result"'),)),
            Node(
                "Call",
                (
                    Node("Name", (Node('"monotonic"'),)),
                    Node("list", (Node("VS:ValSeq"),)),
                ),
            ),
        ),
    )
    print("invocation_constructor_identity", claim_assignment == expected_assignment)
    if solution_function != claim_function or claim_assignment != expected_assignment:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
