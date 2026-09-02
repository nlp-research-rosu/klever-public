#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for flip_case."""

from __future__ import annotations

import hashlib
import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/27-flip-case")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_function("generated_candidate", SCRATCH / "solution.py")

documented_and_boundaries = [
    "Hello",
    "",
    "@AZ[`az{",  # immediately around ASCII A-Z and a-z branches
    "".join(chr(code) for code in range(128)),
    "aZ 123!?\x00\n",
    "éÉ",
    "ß",
    "İıſ",
    "Σσς",
    "ǅǆ",
    "АаЯя",
    "𐐀𐐨",
    "🙂",
    "aßİΣ𐐀🙂Z",
]

rng = random.Random(270027)
alphabet = [
    "\x00",
    "A",
    "Z",
    "a",
    "z",
    "0",
    " ",
    "é",
    "ß",
    "İ",
    "Σ",
    "ς",
    "Я",
    "𐐀",
    "𐐨",
    "🙂",
]
generated = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 80)))
    for _ in range(500)
]

mismatches: list[tuple[str, str, str]] = []
for value in documented_and_boundaries + generated:
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append((repr(value), repr(expected), repr(actual)))

# Exhaust every one-character Python string, including surrogate code points.
single_codepoint_mismatches = 0
for codepoint in range(0x110000):
    value = chr(codepoint)
    if candidate(value) != canonical(value):
        single_codepoint_mismatches += 1
        if len(mismatches) < 20:
            mismatches.append(
                (repr(value), repr(canonical(value)), repr(candidate(value)))
            )

input_digest = hashlib.sha256()
for value in documented_and_boundaries + generated:
    input_digest.update(value.encode("utf-8", "surrogatepass"))
    input_digest.update(b"\0")

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print(f"generated_multichar_cases={len(generated)}")
print("exhaustive_single_codepoint_cases=1114112")
print(f"curated_and_generated_input_sha256={input_digest.hexdigest()}")
print(f"single_codepoint_mismatches={single_codepoint_mismatches}")
print(f"total_recorded_mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")
assert not mismatches
assert single_codepoint_mismatches == 0
print("DIFFERENTIAL=PASS")
