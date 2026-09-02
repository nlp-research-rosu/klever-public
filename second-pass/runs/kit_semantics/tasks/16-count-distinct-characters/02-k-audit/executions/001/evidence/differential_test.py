#!/usr/bin/env python3
"""Independent differential test for HumanEval/16."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
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


canonical_module = load_module("trusted_humaneval_16", Path("/reference/canonical.py"))
candidate_module = load_module("candidate_humaneval_16", Path("/candidate/solution.py"))
canonical = canonical_module.count_distinct_characters
candidate = candidate_module.count_distinct_characters

cases: list[tuple[str, str]] = [
    ("documented_xyzXYZ", "xyzXYZ"),
    ("documented_Jerry", "Jerry"),
    ("empty", ""),
    ("one_lower", "a"),
    ("one_upper", "A"),
    ("case_pair", "aA"),
    ("two_distinct", "ab"),
    ("all_same_mixed", "AaAaAa"),
    ("whitespace", " \t\n\r"),
    ("punctuation", "a-A_a!A?"),
    ("nul", "\x00A\x00a"),
    ("combining_distinct", "éÉe\u0301E\u0301"),
    ("german_sharp_s", "ßẞSSss"),
    ("turkish_i", "Iİıi"),
    ("greek_sigma", "Σσς"),
    ("ligature", "ﬃFFI"),
    ("deseret", "\U00010400\U00010428"),
    ("emoji", "😀😀😃"),
    ("max_code_point", "\U0010ffff\U0010ffff"),
    ("long_repeated", "aA" * 2048),
    ("all_ascii", "".join(chr(codepoint) for codepoint in range(128))),
    ("latin_1", "".join(chr(codepoint) for codepoint in range(256))),
]

rng = random.Random(0x16C0DE)
alphabet = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789 _-!?\t\n"
    "ßẞİıΣσςéÉe\u0301"
    "😀😃\U00010400\U00010428"
)
for length in [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64, 127]:
    for sample in range(20):
        cases.append(
            (
                f"alphabet_random_n{length}_{sample}",
                "".join(rng.choice(alphabet) for _ in range(length)),
            )
        )

for sample in range(500):
    length = rng.randrange(0, 80)
    codepoints: list[int] = []
    while len(codepoints) < length:
        codepoint = rng.randrange(0x110000)
        if 0xD800 <= codepoint <= 0xDFFF:
            continue
        codepoints.append(codepoint)
    cases.append(
        (f"unicode_random_{sample}", "".join(chr(codepoint) for codepoint in codepoints))
    )

input_digest = hashlib.sha256()
mismatches = 0
for index, (label, value) in enumerate(cases):
    encoded = value.encode("utf-8", "surrogatepass")
    input_digest.update(len(encoded).to_bytes(8, "big"))
    input_digest.update(encoded)
    expected = canonical(value)
    actual = candidate(value)
    matches = expected == actual
    if not matches:
        mismatches += 1
    print(
        json.dumps(
            {
                "index": index,
                "label": label,
                "input": value,
                "canonical": expected,
                "candidate": actual,
                "matches": matches,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

print(
    json.dumps(
        {
            "summary": {
                "case_count": len(cases),
                "input_sha256": input_digest.hexdigest(),
                "mismatches": mismatches,
                "oracle": "/reference/canonical.py:count_distinct_characters",
                "candidate": "/candidate/solution.py:count_distinct_characters",
                "seed": "0x16C0DE",
            }
        },
        sort_keys=True,
    )
)
sys.exit(1 if mismatches else 0)
