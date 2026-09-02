#!/usr/bin/env python3
"""Concrete witnesses for the formal preconditions and postconditions."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decode_from(s: str, index: int, accumulator: str) -> str:
    """Independent executable reading of the K decodeFrom equations."""
    while index + 2 < len(s):
        accumulator += s[index + 2] + s[index : index + 2]
        index += 3
    return accumulator + s[index:]


canonical = load_module("canonical_for_witness", Path("/reference/canonical.py"))
generated = load_module("generated_for_witness", Path("/candidate/solution.py"))

loop_witnesses = [
    ("", 0, ""),
    ("bcaefdgh", 3, "abc"),
]
failures = 0
print("LOOP CLAIM WITNESSES")
for s, index, accumulator in loop_witnesses:
    precondition = 0 <= index <= len(s)
    claimed = decode_from(s, index, accumulator)
    print(
        f"S={s!r} I={index} ACC={accumulator!r} "
        f"PRECONDITION={precondition} CLAIMED_RESULT={claimed!r}"
    )
    failures += not precondition

entry_input = "bcaefdgh"
entry_claimed = decode_from(entry_input, 0, "")
canonical_result = canonical.decode_cyclic(entry_input)
generated_result = generated.decode_cyclic(entry_input)
print("PROGRAM CLAIM WITNESS")
print(f"S={entry_input!r} PRECONDITION=<none>")
print(f"CLAIMED_RESULT={entry_claimed!r}")
print(f"CANONICAL_RESULT={canonical_result!r}")
print(f"GENERATED_RESULT={generated_result!r}")
print(
    "ASCII_RESULT_MATCH="
    f"{entry_claimed == canonical_result == generated_result}"
)
failures += not (entry_claimed == canonical_result == generated_result)

unicode_input = "éα中🙂𝄞"
print("UNICODE ADEQUACY WITNESS")
print(f"S={unicode_input!r} PRECONDITION=<none>")
print(f"CANONICAL_RESULT={canonical.decode_cyclic(unicode_input)!r}")
print(f"GENERATED_RESULT={generated.decode_cyclic(unicode_input)!r}")
print(
    "NOTE: rebuilt K result is recorded by semantics_differential.py; "
    "it differs because K STRING.length/substr are UTF-8-byte based."
)

print(f"FAILURE_COUNT: {failures}")
sys.exit(1 if failures else 0)
