#!/usr/bin/env python3
"""Independent differential test for HumanEval 38 decode_cyclic."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


AUDIT_ROOT = Path("/tmp/audit-work/38-decode-cyclic")
EVIDENCE_ROOT = Path("/audit-output/evidence")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", AUDIT_ROOT / "trusted/canonical.py")
candidate = load_module("generated_solution", AUDIT_ROOT / "candidate/solution.py")

# No examples are embedded in prompt.py. These explicit cases cover the
# len(s) < 3 boundary, every residue modulo 3, multiple recursive frames,
# spaces, and non-ASCII Python characters.
explicit_cases = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "abcdefgh",
    "bca",
    "bcaefd",
    "bcaefdg",
    "elho lorwld",
    "\x00a🧪b",
    "🙂é漢字xyz",
]

small_cases = [
    "".join(chars)
    for length in range(8)
    for chars in itertools.product(("a", "b", "🧪"), repeat=length)
]

rng = random.Random(0x38DEC0DE)
random_alphabet = ["a", "Z", "0", " ", "\n", "\x00", "é", "漢", "🙂", "🧪"]
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 81)))
    for _ in range(2000)
]

cases = explicit_cases + small_cases + random_cases
(EVIDENCE_ROOT / "differential-inputs.json").write_text(
    json.dumps(
        {
            "explicit": explicit_cases,
            "exhaustive_alphabet": ["a", "b", "🧪"],
            "exhaustive_lengths": [0, 7],
            "random_seed": "0x38DEC0DE",
            "random_alphabet": random_alphabet,
            "random_length_range": [0, 80],
            "random_count": len(random_cases),
            "all_direct_decode_inputs": cases,
        },
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches = []
roundtrip_failures = []
for text in cases:
    expected = canonical.decode_cyclic(text)
    actual = candidate.decode_cyclic(text)
    if actual != expected:
        mismatches.append(
            {"input": text, "canonical": expected, "candidate": actual}
        )

    encoded = canonical.encode_cyclic(text)
    decoded = candidate.decode_cyclic(encoded)
    if decoded != text:
        roundtrip_failures.append(
            {"source": text, "encoded": encoded, "candidate_decoded": decoded}
        )

print(f"explicit_cases={len(explicit_cases)}")
print(f"exhaustive_small_cases={len(small_cases)}")
print(f"deterministic_random_cases={len(random_cases)}")
print(f"total_direct_comparisons={len(cases)}")
print(f"direct_mismatches={len(mismatches)}")
print(f"roundtrip_checks={len(cases)}")
print(f"roundtrip_failures={len(roundtrip_failures)}")

if mismatches:
    print(json.dumps(mismatches[:20], ensure_ascii=False, indent=2))
if roundtrip_failures:
    print(json.dumps(roundtrip_failures[:20], ensure_ascii=False, indent=2))

sys.exit(1 if mismatches or roundtrip_failures else 0)
