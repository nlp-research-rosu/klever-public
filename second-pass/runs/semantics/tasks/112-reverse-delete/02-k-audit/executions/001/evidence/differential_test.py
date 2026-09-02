#!/usr/bin/env python3
"""Independent differential test for HumanEval 112 reverse_delete."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def strings(alphabet: str, maximum_length: int):
    for length in range(maximum_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-output", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_function(args.canonical, "trusted_canonical_112")
    generated = load_function(args.generated, "generated_solution_112")

    # Named cases cover the documented examples, empty boundaries, both
    # membership branches, all-deleted/all-retained behavior, duplicates,
    # palindrome outcomes, non-ASCII code points, and c-order irrelevance.
    named = [
        ("example_1", "abcde", "ae"),
        ("example_2", "abcdef", "b"),
        ("example_3", "abcdedcba", "ab"),
        ("both_empty", "", ""),
        ("empty_s", "", "anything"),
        ("empty_c_palindrome", "abba", ""),
        ("empty_c_nonpalindrome", "abc", ""),
        ("single_retained", "x", ""),
        ("single_deleted", "x", "x"),
        ("all_deleted", "abc", "cba"),
        ("none_deleted", "racecar", "xyz"),
        ("alternating", "ababab", "b"),
        ("duplicate_membership", "mississippi", "ss"),
        ("unicode_emoji_deleted", "a😀b😀a", "😀"),
        ("unicode_accent_retained", "éaé", "x"),
        ("unicode_membership_order", "😀éaé😀", "é😀"),
    ]

    pairs: list[dict[str, str]] = [
        {"category": category, "s": s, "c": c} for category, s, c in named
    ]

    # Exhaustive small-domain branch coverage: all 364 strings s of length
    # 0..5 and all 40 strings c of length 0..3 over {a,b,c}.
    exhaustive_s = list(strings("abc", 5))
    exhaustive_c = list(strings("abc", 3))
    for s in exhaustive_s:
        for c in exhaustive_c:
            pairs.append({"category": "exhaustive_abc", "s": s, "c": c})

    # Broader deterministic representative inputs.
    seed = 112_2026
    rng = random.Random(seed)
    broad_alphabet = "abcXYZ09😀é"
    for _ in range(3000):
        s = "".join(rng.choice(broad_alphabet) for _ in range(rng.randrange(17)))
        c = "".join(rng.choice(broad_alphabet) for _ in range(rng.randrange(11)))
        pairs.append({"category": "seeded_broad", "s": s, "c": c})

    args.inputs_output.write_text(
        json.dumps(
            {
                "seed": seed,
                "exhaustive_alphabet": "abc",
                "exhaustive_s_max_length": 5,
                "exhaustive_c_max_length": 3,
                "broad_alphabet": broad_alphabet,
                "pairs": pairs,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    category_counts: dict[str, int] = {}
    result_digest = hashlib.sha256()
    for item in pairs:
        category = item["category"]
        s = item["s"]
        c = item["c"]
        category_counts[category] = category_counts.get(category, 0) + 1
        expected = canonical(s, c)
        actual = generated(s, c)
        result_digest.update(
            json.dumps(
                [category, s, c, expected, actual],
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        if expected != actual:
            mismatches.append(
                {
                    "category": category,
                    "s": s,
                    "c": c,
                    "canonical": expected,
                    "generated": actual,
                }
            )

    report = {
        "canonical": str(args.canonical),
        "generated": str(args.generated),
        "input_count": len(pairs),
        "category_counts": category_counts,
        "mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:20],
        "result_digest_sha256": result_digest.hexdigest(),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
