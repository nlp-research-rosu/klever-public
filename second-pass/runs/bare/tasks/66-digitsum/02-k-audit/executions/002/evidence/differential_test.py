#!/usr/bin/env python3
"""Independent CPython differential for HumanEval/66 digitSum."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_entry(
    "trusted_humaneval_66", Path("/tmp/audit-work/66-digitsum-audit/trusted-canonical.py")
)
candidate = load_entry(
    "generated_humaneval_66", Path("/tmp/audit-work/66-digitsum-audit/solution.py")
)

documented = {
    "": 0,
    "abAB": 131,
    "abcCd": 67,
    "helloE": 69,
    "woArBld": 131,
    "aAaaaXa": 153,
}
boundaries = [
    "",
    "@",
    "A",
    "B",
    "Y",
    "Z",
    "[",
    "a",
    "z",
    "@ABYZ[",
    "AZaz09",
]
unicode_witnesses = [
    "É",
    "Ω",
    "İ",
    "Ж",
    "Ա",
    "Ａ",
    "𝔄",
    "aÉz",
    "AΩZ",
]

print("COMMAND: python3 /audit-output/evidence/differential_test.py")
print("oracle=/tmp/audit-work/66-digitsum-audit/trusted-canonical.py:digitSum")
print("candidate=/tmp/audit-work/66-digitsum-audit/solution.py:digitSum")

for text, expected in documented.items():
    oracle_value = canonical(text)
    candidate_value = candidate(text)
    assert oracle_value == expected
    assert candidate_value == expected
    print(
        f"documented input={ascii(text)} expected={expected} "
        f"canonical={oracle_value} candidate={candidate_value} match=yes"
    )

for text in boundaries + unicode_witnesses:
    oracle_value = canonical(text)
    candidate_value = candidate(text)
    print(
        f"boundary input={ascii(text)} canonical={oracle_value} "
        f"candidate={candidate_value} match={'yes' if oracle_value == candidate_value else 'NO'}"
    )

# Exhaust every Python one-character value, including non-ASCII uppercase
# characters.  repr/ascii is used below so lone surrogates remain printable.
singleton_mismatches: list[tuple[int, int, int]] = []
for codepoint in range(0x110000):
    text = chr(codepoint)
    oracle_value = canonical(text)
    candidate_value = candidate(text)
    if oracle_value != candidate_value:
        singleton_mismatches.append((codepoint, oracle_value, candidate_value))

print("singleton_scope=all_1114112_Python_codepoints")
print(f"singleton_mismatch_count={len(singleton_mismatches)}")
for codepoint, oracle_value, candidate_value in singleton_mismatches[:20]:
    print(
        f"singleton_mismatch U+{codepoint:04X} input={ascii(chr(codepoint))} "
        f"canonical={oracle_value} candidate={candidate_value}"
    )

rng = random.Random(660066)
alphabet = list("@ABYZ[az09") + [
    "É",
    "é",
    "Ω",
    "ω",
    "İ",
    "ı",
    "Ж",
    "ж",
    "Ա",
    "ա",
    "Ａ",
    "ａ",
    "𝔄",
    "𝔞",
    "😀",
]
generated_mismatches = 0
first_generated: list[tuple[str, int, int]] = []
for _ in range(2000):
    text = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 33)))
    oracle_value = canonical(text)
    candidate_value = candidate(text)
    if oracle_value != candidate_value:
        generated_mismatches += 1
        if len(first_generated) < 10:
            first_generated.append((text, oracle_value, candidate_value))

print("generated_scope=2000_seeded_strings_length_0_through_32")
print("generated_seed=660066")
print(f"generated_mismatch_count={generated_mismatches}")
for text, oracle_value, candidate_value in first_generated:
    print(
        f"generated_mismatch input={ascii(text)} canonical={oracle_value} "
        f"candidate={candidate_value}"
    )

assert singleton_mismatches, "expected the Unicode-domain implementation divergence"
assert generated_mismatches, "expected representative generated divergences"
print("DIFFERENTIAL_TEST=COMPLETED_WITH_MISMATCHES")
