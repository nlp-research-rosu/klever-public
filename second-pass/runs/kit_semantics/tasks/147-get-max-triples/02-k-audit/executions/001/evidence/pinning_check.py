#!/usr/bin/env python3
"""Mechanically compare submitted MPY function body with the entry-claim closure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(),]'
)


def tokens(path: str) -> list[str]:
    text = Path(path).read_text()
    return TOKEN.findall(text)


def close_of(items: list[str], open_index: int) -> int:
    assert items[open_index] == "("
    depth = 0
    for index in range(open_index, len(items)):
        if items[index] == "(":
            depth += 1
        elif items[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError("unbalanced constructor term")


def term_end(items: list[str], start: int) -> int:
    if start + 1 < len(items) and items[start + 1] == "(":
        return close_of(items, start + 1) + 1
    return start + 1


def submitted_body(items: list[str]) -> list[str]:
    index = items.index("FuncDef")
    assert items[index + 1 : index + 4] == ["(", '"get_max_triples"', ","]
    params_start = index + 4
    assert items[params_start] == "Params"
    params_end = term_end(items, params_start)
    assert items[params_start:params_end] == ["Params", "(", '"n"', ")"]
    assert items[params_end] == ","
    func_close = close_of(items, index + 1)
    return items[params_end + 1 : func_close]


def claim_body(items: list[str]) -> list[str]:
    call = items.index("Call")
    call_end = term_end(items, call)
    assert items[call:call_end] == [
        "Call",
        "(",
        "Name",
        "(",
        '"get_max_triples"',
        ")",
        ",",
        "Int",
        "(",
        "N",
        ")",
        ")",
    ]

    index = items.index("closureVal")
    assert items[index + 1 : index + 4] == ["(", '"n"', ","]
    close = close_of(items, index + 1)
    depth = 0
    separators = []
    for position in range(index + 1, close + 1):
        if items[position] == "(":
            depth += 1
        elif items[position] == ")":
            depth -= 1
        elif items[position] == "," and depth == 1:
            separators.append(position)
    assert len(separators) == 2
    assert items[separators[1] + 1 : close] == ["0"]
    return items[separators[0] + 1 : separators[1]]


if len(sys.argv) != 3:
    raise SystemExit("usage: pinning_check.py solution.mpy spec.k")

mpy = tokens(sys.argv[1])
spec = tokens(sys.argv[2])
body_a = submitted_body(mpy)
body_b = claim_body(spec)
assert body_a == body_b
print(f"solution_tokens={len(mpy)}")
print(f"claim_tokens={len(spec)}")
print(f"function_body_tokens={len(body_a)}")
print("entry_call=Call(Name(\"get_max_triples\"), Int(N))")
print("parameter_list=(\"n\") and closure_parent_scope=0")
print("PINNING CHECK PASS exact constructor-token body identity")
