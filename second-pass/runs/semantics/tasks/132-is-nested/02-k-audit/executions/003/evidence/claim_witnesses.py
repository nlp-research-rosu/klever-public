#!/usr/bin/env python3
"""Ground witnesses for the helper and entry reachability claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


def bseq(value: str) -> str:
    result = "bNil"
    for char in reversed(value):
        result = ("bOpen" if char == "[" else "bClose") + f"({result})"
    return result


def scan_state(initial: int, value: str) -> int:
    state = initial
    for char in value:
        if char == "[":
            state = state + 1 if state < 2 else state
        else:
            state = state + 1 if state > 1 and state < 4 else state
    return state


canonical = load_function("trusted_canonical_witness", "/reference/canonical.py")
generated = load_function(
    "candidate_solution_witness", "/tmp/audit-work/reconstruction/solution.py"
)

entry_values = [
    "",
    "[]",
    "[[]]",
    "[]]]]]]][[[[[]",
    "[[]][[",
    "]]][[[]]",
]
for value in entry_values:
    summary = scan_state(0, value) == 4
    c_value = canonical(value)
    g_value = generated(value)
    assert c_value == g_value == summary
    print(
        "ENTRY",
        f"python={value!r}",
        f"K_BS={bseq(value)}",
        f"nested={str(summary).lower()}",
        f"canonical={c_value}",
        f"generated={g_value}",
    )

loop_values = [
    (0, ""),
    (0, "[[]]"),
    (1, "[]]"),
    (2, "]]"),
    (3, "]"),
    (4, "[[[]"),
]
for initial, value in loop_values:
    final = scan_state(initial, value)
    print(
        "LOOP",
        f"I={initial}",
        f"python_suffix={value!r}",
        f"K_BS={bseq(value)}",
        f"scanState={final}",
        f"claimed_result={str(final == 4).lower()}",
    )

print("SATISFYING_EMPTY_ENTRY=<exact initial cells in spec.k:27-37>")
print("SATISFYING_UNIVERSAL_ENTRY=BS=bNil")
print(
    "SATISFYING_LOOP=I=0,BS=bNil,_CHAR=str(.IntSeq),"
    "_INPUT=str(bCodes(bNil)),with exact global/builtins scopes"
)
print("RESULT all ground substitutions agree")
