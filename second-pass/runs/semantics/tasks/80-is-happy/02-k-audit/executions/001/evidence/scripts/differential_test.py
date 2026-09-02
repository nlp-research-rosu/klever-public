#!/usr/bin/env python3
"""Independent differential test for HumanEval 80 (is_happy)."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


def contract_oracle(s: str) -> bool:
    return len(s) >= 3 and all(len(set(s[i : i + 3])) == 3 for i in range(len(s) - 2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "candidate_solution")

    named = [
        ("empty", ""),
        ("length_1", "a"),
        ("length_2_distinct", "ab"),
        ("length_2_equal", "aa"),
        ("length_3_all_distinct", "abc"),
        ("first_equality_branch", "aab"),
        ("second_equality_branch", "aba"),
        ("third_equality_branch", "abb"),
        ("two_windows_pass", "abcd"),
        ("later_first_equality", "abcaab"),
        ("later_second_equality", "abcaba"),
        ("later_third_equality", "abcabb"),
        ("documented_aabb", "aabb"),
        ("documented_adb", "adb"),
        ("documented_xyy", "xyy"),
        ("repeated_but_happy", "abcabc"),
        ("unicode_distinct", "aβ🙂"),
        ("unicode_unhappy", "a🙂a"),
        ("long_happy", "abc" * 100),
        ("long_late_failure", ("abc" * 100) + "aa"),
    ]

    exhaustive = [
        "".join(chars)
        for length in range(8)
        for chars in itertools.product("abc", repeat=length)
    ]
    rng = random.Random(80080)
    alphabet = "abcdβ🙂"
    generated_inputs = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 101)))
        for _ in range(5000)
    ]

    inputs = [s for _, s in named] + exhaustive + generated_inputs
    args.inputs_out.write_text(
        json.dumps(
            {
                "named": named,
                "exhaustive_alphabet": "abc",
                "exhaustive_lengths": [0, 7],
                "random_seed": 80080,
                "random_alphabet": alphabet,
                "random_count": 5000,
                "random_length_range": [0, 100],
                "all_inputs": inputs,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for s in inputs:
        expected = contract_oracle(s)
        trusted = canonical(s)
        actual = generated(s)
        if (
            type(trusted) is not bool
            or type(actual) is not bool
            or trusted != expected
            or actual != expected
        ):
            mismatches.append(
                {
                    "input": s,
                    "oracle": expected,
                    "canonical": trusted,
                    "generated": actual,
                    "canonical_type": type(trusted).__name__,
                    "generated_type": type(actual).__name__,
                }
            )

    for label, s in named:
        print(
            f"NAMED {label}: input={s!r} "
            f"oracle={contract_oracle(s)!r} "
            f"canonical={canonical(s)!r} generated={generated(s)!r}"
        )
    print(f"TOTAL_INPUTS: {len(inputs)}")
    print(f"UNIQUE_INPUTS: {len(set(inputs))}")
    print(f"MISMATCHES: {len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], ensure_ascii=False, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
