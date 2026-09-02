#!/usr/bin/env python3
"""Ground witnesses for all 13 entry-claim shape preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def mathematical_contract(word: str) -> str:
    vowels = set("aeiouAEIOU")
    for position in range(len(word) - 2, 0, -1):
        if (
            word[position] in vowels
            and word[position - 1] not in vowels
            and word[position + 1] not in vowels
        ):
            return word[position]
    return ""


def main() -> int:
    canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
    candidate = load_entry(
        "scratch_candidate_witness", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    witnesses = [
        (1, "", "length 0"),
        (2, "b", "length 1"),
        (3, "ba", "length 2"),
        (4, "bAb", "suffix consonant-vowel-consonant"),
        (5, "bbb", "length-3 suffix with consonant middle"),
        (6, "bbbb", "recursive consonant-middle; prior -3 consonant"),
        (7, "aabb", "recursive consonant-middle; two prior vowels"),
        (8, "babb", "recursive consonant-middle; prior consonant-vowel"),
        (9, "aab", "length-3 vowel-vowel suffix"),
        (10, "aaab", "recursive vowel-vowel suffix; prior vowel"),
        (11, "baab", "recursive vowel-vowel suffix; prior consonant"),
        (12, "baa", "length-3 consonant-vowel-vowel suffix"),
        (13, "bbaa", "recursive consonant-vowel-vowel suffix"),
    ]
    mismatches = 0
    print("COMMON_STATE: KREST=.K ENV=.Map STACK=.Frames program=solutionProgram")
    for case, word, shape in witnesses:
        expected = mathematical_contract(word)
        canonical_value = canonical(word)
        candidate_value = candidate(word)
        ok = expected == canonical_value == candidate_value
        mismatches += int(not ok)
        print(
            f"case={case:02d} input={word!r} shape={shape!r} "
            f"claimed_result={expected!r} canonical={canonical_value!r} "
            f"candidate={candidate_value!r} match={ok}"
        )
    print(f"TOTAL_WITNESSES: {len(witnesses)}")
    print(f"MISMATCHES: {mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
