#!/usr/bin/env python3
"""Ground satisfying witnesses for all three entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "canonical_witness")
generated = load(Path("/tmp/audit-work/fresh/solution.py"), "generated_witness")


def decode_codes(value: str) -> str:
    return "".join(chr(((ord(char) - 5 - ord("a")) % 26) + ord("a")) for char in value)


inputs = ["", "a", "f", "z", "mjqqt", "fghijklmnopqrstuvwxyzabcde"]
for value in inputs:
    assert all("a" <= character <= "z" for character in value)
    formal = decode_codes(value)
    trusted = canonical.decode_shift(value)
    actual = generated.decode_shift(value)
    assert formal == trusted == actual
    print(f"entry input={value!r} result={formal!r}")

# Loop-claim witness:
# ORIGINAL="az", ACC="q", CS="az", CH="", KONT=.K, standard cells.
acc = "q"
remaining = "az"
loop_result = acc + decode_codes(remaining)
loop_last = remaining[-1] if remaining else ""
assert loop_result == "qvu"
assert loop_last == "z"
print(
    "loop witness ORIGINAL='az' ACC='q' CS='az' CH='' "
    f"result={loop_result!r} final_ch={loop_last!r}"
)

for code in (97, 102, 122):
    encoded = ((code + 5 - 97) % 26) + 97
    decoded = ((encoded - 5 - 97) % 26) + 97
    assert decoded == code
    print(f"char-inverse C={code} encode={encoded} decode={decoded}")
