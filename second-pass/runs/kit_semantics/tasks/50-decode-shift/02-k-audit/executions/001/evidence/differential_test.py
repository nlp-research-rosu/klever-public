#!/usr/bin/env python3
"""Independent generated-vs-canonical differential for the intended domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


WORK = Path("/tmp/audit-work/50-decode-shift")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", WORK / "canonical.py")
generated = load_module("generated_solution", WORK / "solution.py")
prompt = load_module("trusted_prompt", WORK / "prompt.py")

alphabet = "abcdefghijklmnopqrstuvwxyz"
cases: list[str] = [
    "",
    "a",
    "e",
    "f",
    "z",
    "ae",
    "ef",
    "fa",
    alphabet,
    alphabet[::-1],
    "a" * 256,
    "e" * 256,
    "f" * 256,
    "z" * 256,
]
cases.extend(alphabet)
cases.extend(
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
)

rng = random.Random(0x50DEC0DE)
for length in (4, 5, 7, 16, 31, 64, 127):
    for _ in range(300):
        cases.append("".join(rng.choice(alphabet) for _ in range(length)))

mismatches: list[tuple[str, str, str]] = []
for encoded in cases:
    expected = canonical.decode_shift(encoded)
    actual = generated.decode_shift(encoded)
    if actual != expected:
        mismatches.append((encoded, expected, actual))

inverse_cases = 0
for original in cases:
    encoded = prompt.encode_shift(original)
    actual = generated.decode_shift(encoded)
    if actual != original:
        mismatches.append((f"encode_shift({original!r})", original, actual))
    inverse_cases += 1

print(
    "documented_examples=0 "
    "(the trusted prompt provides no explicit example assertions)"
)
print(
    "boundary_inputs="
    "empty,a,e,f,z,wrap-transition-pairs,full-alphabet,long-uniform"
)
print(
    f"direct_cases={len(cases)} inverse_cases={inverse_cases} "
    f"mismatches={len(mismatches)}"
)
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    raise SystemExit(1)
print("DIFFERENTIAL PASS")
