#!/usr/bin/env python3
"""Independent candidate/canonical differential and supplied-model gap check."""

from __future__ import annotations

import importlib.util
import inspect
import random
import sys
from pathlib import Path


def load_function(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function("candidate_solution", Path("/candidate/solution.py"))

documented = ["", "abAB", "abcCd", "helloE", "woArBld", "aAaaaXa"]
boundaries = [
    "@",
    "A",
    "Z",
    "[",
    "`",
    "a",
    "z",
    "{",
    "\x00A\nZ\U0010ffff",
    "ÄΩİßǅ𝔄",
    "\ud800A\udfff",
]

rng = random.Random(660029)
random_strings: list[str] = []
for length in [0, 1, 2, 3, 7, 31, 128, 1024]:
    for _ in range(25):
        random_strings.append(
            "".join(chr(rng.randrange(0x110000)) for _ in range(length))
        )

candidate_mismatches: list[tuple[str, int, int]] = []
for text in documented + boundaries + random_strings:
    got = candidate(text)
    expected = canonical(text)
    if got != expected:
        candidate_mismatches.append((repr(text), got, expected))

single_codepoint_mismatch = None
model_gap_witness = None
model_gap_count = 0
for codepoint in range(sys.maxunicode + 1):
    text = chr(codepoint)
    got = candidate(text)
    expected = canonical(text)
    if got != expected and single_codepoint_mismatch is None:
        single_codepoint_mismatch = (codepoint, got, expected)
    model_result = codepoint if 65 <= codepoint <= 90 else 0
    if expected != model_result:
        model_gap_count += 1
        if model_gap_witness is None:
            model_gap_witness = (
                codepoint,
                repr(text),
                expected,
                model_result,
                text.isupper(),
            )

print(f"canonical_signature={inspect.signature(canonical)}")
print(f"candidate_signature={inspect.signature(candidate)}")
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"random_strings={len(random_strings)}")
print(f"single_codepoints={sys.maxunicode + 1}")
print(f"candidate_mismatch_count={len(candidate_mismatches)}")
print(f"candidate_first_mismatch={candidate_mismatches[:1]!r}")
print(f"single_codepoint_first_mismatch={single_codepoint_mismatch!r}")
print(f"model_gap_single_codepoint_count={model_gap_count}")
print(f"model_gap_first_witness={model_gap_witness!r}")

if candidate_mismatches or single_codepoint_mismatch is not None:
    raise SystemExit(1)
