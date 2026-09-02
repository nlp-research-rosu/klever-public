#!/usr/bin/env python3
"""Concrete satisfying witnesses for each of the 13 entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path("/tmp/audit-work/118-get-closest-vowel")


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def main() -> int:
    canonical = load_entry(ROOT / "reference" / "canonical.py", "witness_canonical")
    candidate = load_entry(
        ROOT / "candidate-src" / "solution.py", "witness_candidate"
    )
    # Each tuple is (claim number, satisfying Chars/word witness, instantiated RHS).
    witnesses = [
        (1, "", ""),
        (2, "b", ""),
        (3, "bb", ""),
        (4, "bab", "a"),
        (5, "bbb", ""),
        (6, "bbbb", ""),
        (7, "aabb", ""),
        (8, "babb", "a"),
        (9, "aab", ""),
        (10, "aaab", ""),
        (11, "baab", ""),
        (12, "baa", ""),
        (13, "bbaa", ""),
    ]
    mismatches = 0
    for claim, word, rhs in witnesses:
        canonical_result = canonical(word)
        candidate_result = candidate(word)
        good = canonical_result == candidate_result == rhs
        if not good:
            mismatches += 1
        print(
            f"CLAIM={claim:02d} WORD={word!r} "
            f"CLAIM_RHS={rhs!r} CANONICAL={canonical_result!r} "
            f"CANDIDATE={candidate_result!r} MATCH={good}"
        )
    print(f"WITNESSES={len(witnesses)}")
    print(f"MISMATCHES={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
