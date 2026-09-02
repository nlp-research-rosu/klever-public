#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical")
generated = load(Path("/tmp/audit-work/fresh/solution.py"), "generated_solution")

cases: list[tuple[str, str]] = []


def add(label: str, value: str) -> None:
    cases.append((label, value))


add("empty", "")
for character in string.ascii_lowercase:
    add(f"single-{character}", character)
add("branch-below-subtraction", "abcde")
add("branch-at-subtraction", "f")
add("branch-above-subtraction", "ghijklmnopqrstuvwxyz")
add("alphabet", string.ascii_lowercase)
add("wrapped-alphabet", "fghijklmnopqrstuvwxyzabcde")
add("repetitions", "aaaaazzzzzfffff")
add("long-boundary-pattern", ("afz" * 1000))

# Exhaust all lowercase strings through length three.
for length in range(4):
    for chars in itertools.product(string.ascii_lowercase, repeat=length):
        add(f"exhaustive-len-{length}", "".join(chars))

# Fixed-seed representative generated inputs, including larger values.
rng = random.Random(0x50DEC0DE)
for length in (4, 5, 8, 16, 31, 32, 64, 127, 256, 1024):
    for sample in range(25):
        add(
            f"random-len-{length}-sample-{sample}",
            "".join(rng.choice(string.ascii_lowercase) for _ in range(length)),
        )

mismatches = []
inverse_failures = []
for label, value in cases:
    expected = canonical.decode_shift(value)
    observed = generated.decode_shift(value)
    if observed != expected:
        mismatches.append((label, value, expected, observed))

# The prompt's encoder supplies an independent contract check on lowercase plaintext.
plaintexts = ["", string.ascii_lowercase, "hello", "xyz", "a" * 257]
for value in plaintexts:
    encoded = canonical.encode_shift(value)
    decoded = generated.decode_shift(encoded)
    if decoded != value:
        inverse_failures.append((value, encoded, decoded))

print(f"cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
print(f"inverse_cases={len(plaintexts)}")
print(f"inverse_failures={len(inverse_failures)}")
if mismatches:
    print(f"first_mismatch={mismatches[0]!r}")
if inverse_failures:
    print(f"first_inverse_failure={inverse_failures[0]!r}")
raise SystemExit(bool(mismatches or inverse_failures))
