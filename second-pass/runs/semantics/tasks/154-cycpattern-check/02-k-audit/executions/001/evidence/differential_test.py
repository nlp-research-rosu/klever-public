#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for problem 154."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/154-cycpattern-check/candidate/solution.py")
OUTPUT_PATH = Path("/audit-output/evidence/differential_cases.json")

EXAMPLES = [
    ("abcd", "abd", False),
    ("hello", "ell", True),
    ("whassup", "psus", False),
    ("abab", "baa", True),
    ("efef", "eeff", False),
    ("himenss", "simen", True),
]

BOUNDARIES = [
    ("", ""),
    ("a", ""),
    ("", "a"),
    ("a", "a"),
    ("a", "b"),
    ("ab", "ba"),
    ("ba", "ab"),
    ("ab", "aba"),
    ("aba", "aba"),
    ("aaaa", "aa"),
    ("abab", "baba"),
    ("xxcabyy", "abc"),
    ("xxbcayy", "abc"),
    ("xxabcxyy", "abcx"),
    ("éλé", "λé"),
]


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


def all_words(alphabet: str, maximum_length: int):
    for length in range(maximum_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical_154")
    candidate = load_function(CANDIDATE_PATH, "submitted_solution_154")

    cases: list[tuple[str, str, str]] = []
    for a, b, _expected in EXAMPLES:
        cases.append((a, b, "documented-example"))
    for a, b in BOUNDARIES:
        cases.append((a, b, "explicit-boundary"))

    words = list(all_words("ab", 5))
    for a in words:
        for b in words:
            cases.append((a, b, "exhaustive-ab-length-0-through-5"))

    rng = random.Random(154)
    for _ in range(300):
        a = "".join(rng.choice("abc") for _ in range(rng.randrange(0, 10)))
        b = "".join(rng.choice("abc") for _ in range(rng.randrange(0, 8)))
        cases.append((a, b, "deterministic-generated-seed-154"))

    unique: dict[tuple[str, str], str] = {}
    for a, b, category in cases:
        unique.setdefault((a, b), category)

    records = []
    mismatches = []
    example_errors = []
    for (a, b), category in unique.items():
        expected = canonical(a, b)
        actual = candidate(a, b)
        record = {
            "a": a,
            "b": b,
            "category": category,
            "canonical": expected,
            "candidate": actual,
            "match": actual == expected,
        }
        records.append(record)
        if actual != expected:
            mismatches.append(record)

    for a, b, expected in EXAMPLES:
        canonical_value = canonical(a, b)
        candidate_value = candidate(a, b)
        if canonical_value != expected or candidate_value != expected:
            example_errors.append(
                {
                    "a": a,
                    "b": b,
                    "stated": expected,
                    "canonical": canonical_value,
                    "candidate": candidate_value,
                }
            )

    serialized_records = json.dumps(records, ensure_ascii=False, sort_keys=True)
    payload = {
        "oracle": str(CANONICAL_PATH),
        "candidate": str(CANDIDATE_PATH),
        "scope": {
            "documented_examples": len(EXAMPLES),
            "explicit_boundaries": len(BOUNDARIES),
            "exhaustive_alphabet": "ab",
            "exhaustive_max_length_each_argument": 5,
            "deterministic_generated_cases_requested": 300,
            "random_seed": 154,
        },
        "unique_case_count": len(records),
        "record_sha256": hashlib.sha256(serialized_records.encode("utf-8")).hexdigest(),
        "mismatch_count": len(mismatches),
        "example_error_count": len(example_errors),
        "example_errors": example_errors,
        "mismatches": mismatches,
        "records": records,
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    mismatch_categories: dict[str, int] = {}
    for mismatch in mismatches:
        key = "b-empty" if mismatch["b"] == "" else "other"
        mismatch_categories[key] = mismatch_categories.get(key, 0) + 1

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"unique_cases={len(records)}")
    print(f"record_sha256={payload['record_sha256']}")
    print(f"documented_example_errors={len(example_errors)}")
    print(f"mismatches={len(mismatches)}")
    print(f"mismatch_categories={json.dumps(mismatch_categories, sort_keys=True)}")
    print(
        "first_mismatches="
        + json.dumps(mismatches[:20], ensure_ascii=False, sort_keys=True)
    )
    print(f"complete_results={OUTPUT_PATH}")
    return 1 if mismatches or example_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
