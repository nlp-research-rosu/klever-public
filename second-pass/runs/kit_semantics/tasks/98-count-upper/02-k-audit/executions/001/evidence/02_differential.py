#!/usr/bin/env python3
"""Independent differential test for HumanEval 98 count_upper."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_upper


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/98-count-upper/solution.py"), "generated_solution"
)

documented_and_boundaries = [
    "aBCdEf",
    "abcdefg",
    "dBBE",
    "",
    "A",
    "B",
    "a",
    "AA",
    "BA",
    "AB",
    "AAB",
    "BAA",
    "AEIOU",
    "aE",
    "Aa",
    "\x00A\x00E",
    "🙂A🙂E",
    "ÅE🙂I",
    "A🙂E🙂I🙂O🙂U",
    "a" * 10_000,
    "A" * 10_001,
]

# Exhaustive short strings cover loop zero/one/multiple iterations, odd/even
# lengths, membership true/false, and uppercase vowels at both index parities.
alphabet = "AEIOUaeiouBZ🙂"
exhaustive = (
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(alphabet, repeat=length)
)

# Reproducible broader Unicode sample, including NUL, BMP, astral, and lone
# surrogate code points (all are legal Python str elements).
rng = random.Random(98_2026_07_29)
code_points = [
    0,
    1,
    31,
    32,
    65,
    69,
    73,
    79,
    85,
    90,
    97,
    0x7F,
    0x80,
    0xC5,
    0x3A9,
    0xD800,
    0xE000,
    0x1F642,
    0x10FFFF,
]
random_cases = [
    "".join(chr(rng.choice(code_points)) for _ in range(rng.randrange(0, 129)))
    for _ in range(20_000)
]

cases = list(documented_and_boundaries)
cases.extend(exhaustive)
cases.extend(random_cases)

mismatches = []
result_counts: dict[int, int] = {}
input_digest = hashlib.sha256()
for index, value in enumerate(cases):
    expected = canonical(value)
    actual = generated(value)
    result_counts[expected] = result_counts.get(expected, 0) + 1
    encoded = json.dumps(value, ensure_ascii=True).encode()
    input_digest.update(len(encoded).to_bytes(8, "big"))
    input_digest.update(encoded)
    if actual != expected:
        mismatches.append((index, repr(value), expected, actual))
        if len(mismatches) == 20:
            break

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print("exhaustive_alphabet=" + json.dumps(alphabet, ensure_ascii=True))
print("exhaustive_lengths=0..4")
print(f"random_seed={98_2026_07_29}")
print(f"random_cases={len(random_cases)} random_length_range=0..128")
print(f"total_cases={len(cases)}")
print(f"input_sha256={input_digest.hexdigest()}")
print(f"canonical_result_histogram={dict(sorted(result_counts.items()))}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches)
