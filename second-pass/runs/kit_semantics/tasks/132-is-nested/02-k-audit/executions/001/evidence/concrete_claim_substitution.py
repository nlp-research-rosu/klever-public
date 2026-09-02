#!/usr/bin/env python3
"""Ground instances of the SPEC.program pre/postcondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


def nested_step(code: int, state: int) -> int:
    if state < 2:
        return state + 1 if code == 91 else state
    if state < 4:
        return state + 1 if code == 93 else state
    return state


def nested_result(value: str) -> bool:
    state = 0
    for character in value:
        state = nested_step(ord(character), state)
    return state == 4


canonical = load(Path("/reference/canonical.py"), "ground_canonical")
candidate = load(Path("/candidate/solution.py"), "ground_candidate")
witnesses = ["", "[", "[[", "[[]", "[[]]", "[]]]]]]][[[[[]", "[[]][["]
failures = 0
for value in witnesses:
    codes = [ord(character) for character in value]
    precondition = all(code in (91, 93) for code in codes)
    proof_side = nested_result(value)
    canonical_side = canonical(value)
    candidate_side = candidate(value)
    matches = (
        precondition
        and proof_side == canonical_side
        and proof_side == candidate_side
        and type(candidate_side) is bool
    )
    failures += not matches
    print(
        f"value={value!r} codes={codes!r} bracketInput={precondition} "
        f"nestedResult={proof_side} canonical={canonical_side} "
        f"candidate={candidate_side} match={matches}"
    )
print(f"ground_witnesses={len(witnesses)} failures={failures}")
raise SystemExit(1 if failures else 0)
