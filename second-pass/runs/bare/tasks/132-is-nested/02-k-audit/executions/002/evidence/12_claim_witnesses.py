#!/usr/bin/env python3
"""Concrete realizability and postcondition witnesses for all five claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


canonical = load_function(Path("/reference/canonical.py"), "witness_canonical_132")
submitted = load_function(
    Path("/tmp/audit-work/132-is-nested/solution.py"), "witness_submitted_132"
)


def scan(state: int, suffix: str) -> bool:
    for character in suffix:
        if state == 0:
            state = 1 if character == "[" else 0
        elif state == 1:
            state = 2 if character == "[" else 1
        elif state == 2:
            state = 2 if character == "[" else 3
        elif state == 3:
            if character == "]":
                return True
    return False


prefixes = {
    0: ("", ""),      # before the first iteration
    1: ("[", "["),    # after consuming one left bracket
    2: ("[[", "["),   # after consuming two left brackets
    3: ("[[]", "]"),  # after consuming the first right bracket
}
suffixes = ["", "[", "]", "[]", "]]", "[[]]", "][[]"]

mismatches = 0
for state in range(4):
    prefix, current = prefixes[state]
    for suffix in suffixes:
        original = prefix + suffix
        claimed = scan(state, suffix)
        trusted = canonical(original)
        generated = submitted(original)
        print(
            f"LOOP_CLAIM state={state} ORIG={original!r} CUR={current!r} "
            f"BS={suffix!r} claimed_scan={claimed} "
            f"canonical={trusted} submitted={generated}"
        )
        if claimed != trusted or claimed != generated:
            mismatches += 1

entry_inputs = ["", "[", "]", "[[]", "[[]]", "[][]", "[[][]]", "[[]][["]
for text in entry_inputs:
    claimed = scan(0, text)
    trusted = canonical(text)
    generated = submitted(text)
    print(
        f"ENTRY_CLAIM BS={text!r} claimed_scan={claimed} "
        f"canonical={trusted} submitted={generated}"
    )
    if claimed != trusted or claimed != generated:
        mismatches += 1

print(f"loop_witnesses={4 * len(suffixes)} entry_witnesses={len(entry_inputs)}")
print(f"mismatch_count={mismatches}")
assert mismatches == 0
print("CLAIM_WITNESSES_OK")
