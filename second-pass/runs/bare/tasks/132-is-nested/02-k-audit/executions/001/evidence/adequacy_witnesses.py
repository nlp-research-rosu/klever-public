#!/usr/bin/env python3
"""Ground witnesses for the entry claim and all four loop claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


def scan(state: int, suffix: str) -> bool:
    for character in suffix:
        if state == 0:
            state = 1 if character == "[" else 0
        elif state == 1:
            state = 2 if character == "[" else 1
        elif state == 2:
            state = 2 if character == "[" else 3
        elif state == 3 and character == "]":
            return True
    return False


def execute_loop_from_state(state: int, suffix: str) -> bool:
    for bracket in suffix:
        if bracket == "[":
            if state < 2:
                state = state + 1
        else:
            if state == 2:
                state = 3
            elif state == 3:
                return True
    return False


candidate = load_entry(
    Path("/tmp/audit-work/source/solution.py"), "witness_candidate"
)
canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical"
)

entry_inputs = ["", "[[]]", "[]]]]]]][[[[[]"]
for text in entry_inputs:
    print(
        "ENTRY "
        f"BS={text!r} scan={scan(0, text)} "
        f"candidate={candidate(text)} canonical={canonical(text)}"
    )

loop_witnesses = [(0, "[[]]"), (1, "[]]"), (2, "]]"), (3, "]")]
for state, suffix in loop_witnesses:
    summary = scan(state, suffix)
    execution = execute_loop_from_state(state, suffix)
    print(
        "LOOP "
        f"state={state} BS={suffix!r} ORIG='' CUR='' "
        f"scan={summary} executed_suffix={execution}"
    )
    if summary != execution:
        raise SystemExit(1)

if any(
    scan(0, text) != candidate(text)
    or scan(0, text) != canonical(text)
    for text in entry_inputs
):
    raise SystemExit(1)

print("ALL_WITNESSES_SATISFY_CLAIM_SHAPES_AND_RESULTS")
