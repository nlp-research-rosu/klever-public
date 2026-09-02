#!/usr/bin/env python3
"""Independent candidate/canonical differential and contract-property checks."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


EVIDENCE_DIR = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/palindrome-audit/candidate/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_expected(value: str) -> str:
    """Directly search all suffix starts, independent of either implementation."""
    for index in range(len(value) + 1):
        suffix = value[index:]
        if suffix == suffix[::-1]:
            return value + value[:index][::-1]
    raise AssertionError("the empty suffix is always palindromic")


def suffix_start(value: str) -> int:
    for index in range(len(value) + 1):
        if value[index:] == value[index:][::-1]:
            return index
    raise AssertionError("unreachable")


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    candidate = load_module("audited_candidate", CANDIDATE_PATH)

    categories: dict[str, list[str]] = {
        "documented_examples": ["", "cat", "cata"],
        "empty_and_boundaries": [
            "",
            "a",
            "aa",
            "ab",
            "aba",
            "abba",
            "abc",
            "abcd",
            "aaaa",
            "aab",
            "baa",
            "race",
            "abac",
        ],
        "unicode_and_text_boundaries": [
            "å",
            "åβ",
            "βåβ",
            "🙂🙃",
            "🙂a🙂",
            "e\u0301",
            "e\u0301e",
            "\u0000",
            "\u0000a",
            " a ",
            "\n\t",
        ],
    }

    exhaustive: list[str] = []
    for length in range(0, 8):
        exhaustive.extend(
            "".join(chars)
            for chars in itertools.product("abc", repeat=length)
        )
    categories["exhaustive_abc_lengths_0_through_7"] = exhaustive

    rng = random.Random(20260724)
    random_cases = [
        "".join(rng.choice("abcdXYZ09🙂") for _ in range(rng.randrange(0, 41)))
        for _ in range(2000)
    ]
    categories["seeded_random_2000_lengths_0_through_40"] = random_cases

    all_cases: list[str] = []
    for category_cases in categories.values():
        all_cases.extend(category_cases)

    mismatches: list[dict[str, object]] = []
    branch_starts: set[int] = set()
    for value in all_cases:
        canonical_result = canonical.make_palindrome(value)
        candidate_result = candidate.make_palindrome(value)
        expected_result = independent_expected(value)
        branch_starts.add(suffix_start(value))
        if (
            canonical_result != candidate_result
            or candidate_result != expected_result
            or not candidate_result.startswith(value)
            or candidate_result != candidate_result[::-1]
        ):
            mismatches.append(
                {
                    "input": value,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                    "independent_expected": expected_result,
                }
            )

    inputs_path = EVIDENCE_DIR / "differential-inputs.json"
    inputs_path.write_text(
        json.dumps(
            {
                "oracle": str(CANONICAL_PATH),
                "candidate": str(CANDIDATE_PATH),
                "random_seed": 20260724,
                "categories": categories,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"total_cases_with_category_duplicates={len(all_cases)}")
    print(f"unique_cases={len(set(all_cases))}")
    print(f"observed_first_palindromic_suffix_starts={sorted(branch_starts)}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], ensure_ascii=False, indent=2))
        return 1
    print("RESULT: all candidate, canonical, and independent results agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
