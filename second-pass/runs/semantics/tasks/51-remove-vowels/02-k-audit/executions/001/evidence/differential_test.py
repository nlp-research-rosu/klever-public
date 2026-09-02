#!/usr/bin/env python3
"""Independent differential test for HumanEval 51 remove_vowels."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from pathlib import Path


DOCUMENTED = [
    "",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
]

BOUNDARY_AND_BRANCH = [
    "a",
    "A",
    "e",
    "E",
    "i",
    "I",
    "o",
    "O",
    "u",
    "U",
    "b",
    "Z",
    "ab",
    "ba",
    "bab",
    "aba",
    "AEIOU",
    "aeiou",
    "bcdfg",
    "\x00a\x00",
    "\na\n",
    " a\tE ",
    "áéíóú",
    "ÄËÏÖÜ",
    "İıſKÅ",
    "😀a🚀E",
    "a\u0301e\u0301",
]


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    canonical = load_entry("audit_canonical", args.canonical)
    candidate = load_entry("audit_candidate", args.candidate)

    rng = random.Random(510051)
    alphabet = (
        "aeiouAEIOUbcdfgBCDFG0123 \t\n\x00"
        "áéíóúÄËÏÖÜİıſKÅ😀🚀\u0301"
    )
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 65)))
        for _ in range(5000)
    ]
    curated = DOCUMENTED + BOUNDARY_AND_BRANCH + generated

    mismatches: list[dict[str, str]] = []
    digest = hashlib.sha256()
    for text in curated:
        digest.update(text.encode("utf-8", "surrogatepass"))
        digest.update(b"\x00")
        expected = canonical(text)
        actual = candidate(text)
        if actual != expected:
            mismatches.append(
                {"input": repr(text), "canonical": repr(expected), "candidate": repr(actual)}
            )

    unicode_singletons = 0
    unicode_digest = hashlib.sha256()
    for codepoint in range(0x110000):
        if 0xD800 <= codepoint <= 0xDFFF:
            continue
        text = chr(codepoint)
        unicode_singletons += 1
        expected = canonical(text)
        actual = candidate(text)
        unicode_digest.update(codepoint.to_bytes(4, "big"))
        unicode_digest.update(expected.encode("utf-8"))
        unicode_digest.update(b"\x00")
        if actual != expected:
            mismatches.append(
                {"input": f"U+{codepoint:04X}", "canonical": repr(expected), "candidate": repr(actual)}
            )

    report = {
        "documented_cases": len(DOCUMENTED),
        "boundary_and_branch_cases": len(BOUNDARY_AND_BRANCH),
        "seed": 510051,
        "generated_cases": len(generated),
        "generated_max_length": 64,
        "curated_and_generated_total": len(curated),
        "curated_corpus_sha256": digest.hexdigest(),
        "unicode_singletons": unicode_singletons,
        "unicode_result_sha256": unicode_digest.hexdigest(),
        "mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:20],
    }
    print(json.dumps(report, indent=2, ensure_ascii=True, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
