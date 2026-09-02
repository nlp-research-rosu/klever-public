#!/usr/bin/env python3
"""Independent differential test for HumanEval 7.

The oracle is loaded from the trusted /reference/canonical.py. The candidate
entry point is loaded from the clean scratch copy of solution.py. Test cases
include documented examples, hand-selected branch boundaries, an exhaustive
small alphabet, and deterministic generated Unicode cases.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Callable, List


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/7-filter-by-substring/solution.py")
CASES_PATH = Path("/audit-output/evidence/differential_cases.json")


def load_entry(path: Path, module_name: str) -> Callable[[List[str], str], List[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    candidate = load_entry(CANDIDATE_PATH, "scratch_candidate")

    named_cases = [
        ("documented-empty", [], "a"),
        ("documented-example", ["abc", "bacd", "cde", "array"], "a"),
        ("empty-needle", ["", "x", "x", "α"], ""),
        ("empty-haystack-nonempty-needle", [""], "a"),
        ("exact-match", ["needle", "needlex", "xneedle", "xneedlex"], "needle"),
        ("start-middle-end-absent", ["abxx", "xxabxx", "xxab", "xxxx"], "ab"),
        ("duplicates-order", ["ba", "a", "ba", "z", "a"], "a"),
        ("unicode", ["café", "CAFE", "😀x", "x😀", "e\u0301"], ["é"][0]),
        ("nul-character", ["a\u0000b", "\u0000", "ab"], "\u0000"),
        ("needle-longer", ["a", "ab", ""], "abc"),
    ]

    small_strings = ["", "a", "b", "aa", "ab", "ba", "bb"]
    small_needles = ["", "a", "b", "aa", "ab", "c"]
    exhaustive_cases = []
    for length in range(4):
        for values in itertools.product(small_strings, repeat=length):
            for needle in small_needles:
                exhaustive_cases.append((list(values), needle))

    rng = random.Random(7007)
    random_cases = []
    alphabet = ["a", "b", "é", "\u0301", "😀", "\u0000"]
    for _ in range(2000):
        strings = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 7)))
            for _ in range(rng.randrange(0, 7))
        ]
        needle = "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(0, 5))
        )
        random_cases.append((strings, needle))

    recorded = {
        "oracle": str(CANONICAL_PATH),
        "candidate": str(CANDIDATE_PATH),
        "named": [
            {"name": name, "strings": strings, "substring": needle}
            for name, strings, needle in named_cases
        ],
        "exhaustive": {
            "string_values": small_strings,
            "needle_values": small_needles,
            "list_lengths": [0, 1, 2, 3],
            "case_count": len(exhaustive_cases),
        },
        "generated": {
            "seed": 7007,
            "alphabet": alphabet,
            "case_count": len(random_cases),
            "max_list_length": 6,
            "max_string_length": 6,
            "max_needle_length": 4,
        },
    }
    CASES_PATH.write_text(
        json.dumps(recorded, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    mismatches = []
    total = 0
    for label, strings, needle in named_cases:
        total += 1
        expected = canonical(strings, needle)
        actual = candidate(strings, needle)
        if actual != expected:
            mismatches.append((label, strings, needle, expected, actual))

    for index, (strings, needle) in enumerate(exhaustive_cases):
        total += 1
        expected = canonical(strings, needle)
        actual = candidate(strings, needle)
        if actual != expected:
            mismatches.append(
                (f"exhaustive-{index}", strings, needle, expected, actual)
            )

    for index, (strings, needle) in enumerate(random_cases):
        total += 1
        expected = canonical(strings, needle)
        actual = candidate(strings, needle)
        if actual != expected:
            mismatches.append(
                (f"generated-{index}", strings, needle, expected, actual)
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_cases={len(exhaustive_cases)}")
    print(f"generated_cases={len(random_cases)}")
    print(f"total_cases={total}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print(repr(mismatch))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
