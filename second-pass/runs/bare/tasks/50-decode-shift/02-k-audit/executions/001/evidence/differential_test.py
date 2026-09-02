#!/usr/bin/env python3
"""Independent differential tests for HumanEval 50 decode_shift."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py TRUSTED_CANONICAL GENERATED_SOLUTION")
        return 64

    canonical = load_module("trusted_canonical", Path(sys.argv[1]))
    generated = load_module("generated_solution", Path(sys.argv[2]))
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    named_cases = {
        "empty": "",
        "below_wrap": "a",
        "wrap_edge_low": "e",
        "wrap_edge_high": "f",
        "upper_boundary": "z",
        "all_letters": alphabet,
        "reverse_letters": alphabet[::-1],
        "mixed_boundaries": "aefzfae",
        "candidate_smoke_1": "fgh",
        "candidate_smoke_2": "eabz",
        "repeated": "aaaaafffffzzzzz",
    }

    cases = list(named_cases.values())
    exhaustive_count = 0
    for length in range(4):
        for chars in itertools.product(alphabet, repeat=length):
            cases.append("".join(chars))
            exhaustive_count += 1

    rng = random.Random(0x50DEC0DE)
    random_cases = []
    for length in [4, 5, 7, 16, 31, 64, 127, 256]:
        for _ in range(25):
            value = "".join(rng.choice(alphabet) for _ in range(length))
            cases.append(value)
            random_cases.append(value)

    mismatches = []
    for encoded in cases:
        expected = canonical.decode_shift(encoded)
        actual = generated.decode_shift(encoded)
        if actual != expected:
            mismatches.append(
                {"encoded": encoded, "canonical": expected, "generated": actual}
            )

    inversion_mismatches = []
    inversion_sources = list(named_cases.values()) + random_cases
    for source in inversion_sources:
        encoded = canonical.encode_shift(source)
        canonical_decoded = canonical.decode_shift(encoded)
        generated_decoded = generated.decode_shift(encoded)
        if canonical_decoded != source or generated_decoded != source:
            inversion_mismatches.append(
                {
                    "source": source,
                    "encoded": encoded,
                    "canonical": canonical_decoded,
                    "generated": generated_decoded,
                }
            )

    report = {
        "oracle": str(Path(sys.argv[1])),
        "generated": str(Path(sys.argv[2])),
        "intended_domain": "lowercase ASCII encoded strings",
        "named_cases": named_cases,
        "exhaustive_scope": "all lowercase strings of lengths 0 through 3",
        "exhaustive_count": exhaustive_count,
        "seed": "0x50DEC0DE",
        "random_count": len(random_cases),
        "total_decode_comparisons": len(cases),
        "decode_mismatch_count": len(mismatches),
        "inversion_comparisons": len(inversion_sources),
        "inversion_mismatch_count": len(inversion_mismatches),
        "first_decode_mismatches": mismatches[:10],
        "first_inversion_mismatches": inversion_mismatches[:10],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches or inversion_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
