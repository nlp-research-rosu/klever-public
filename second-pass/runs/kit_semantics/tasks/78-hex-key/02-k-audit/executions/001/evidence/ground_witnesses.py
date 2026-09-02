#!/usr/bin/env python3
"""Concrete satisfying instances of the symbolic entry claim."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


if len(sys.argv) != 3:
    raise SystemExit("usage: ground_witnesses.py CANONICAL.py SOLUTION.py")

canonical = load(Path(sys.argv[1]), "ground_canonical")
solution = load(Path(sys.argv[2]), "ground_solution")
prime_codes = frozenset((50, 51, 53, 55, 66, 68))

witnesses = ("", "2", "A", "D", "AB", "ABED1A33")
for value in witnesses:
    codes = tuple(ord(character) for character in value)
    claimed_hex_count = sum(code in prime_codes for code in codes)
    trusted_result = canonical(value)
    candidate_result = solution(value)
    print(
        f"value={value!r} CS={codes!r} "
        f"hexCount={claimed_hex_count} canonical={trusted_result} "
        f"candidate={candidate_result}"
    )
    assert claimed_hex_count == trusted_result == candidate_result

print(
    "SATISFYING_ENTRY_STATE: env=0; scopes={-1:builtinsScope, "
    "0:scope(hex_key->exact closure,parent(-1))}; scopeLoc=1; "
    "heap=.Map; heapLoc=0; stack=.List; ret=noRet; exc=NoExc; exit-code=0"
)
