#!/usr/bin/env python3
"""Independent differential/property tests for HumanEval 14 all_prefixes."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/run-002")
INPUT_DUMP = Path("/audit-output/evidence/stage2/differential-inputs.json")


def import_from(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_oracle(value: str) -> list[str]:
    return [value[:end] for end in range(1, len(value) + 1)]


def main() -> int:
    canonical_module = import_from("trusted_canonical", WORK / "canonical.py")
    candidate_module = import_from("generated_solution", WORK / "solution.py")
    canonical = canonical_module.all_prefixes
    candidate = candidate_module.all_prefixes

    documented_and_boundaries = [
        "abc",
        "",
        "a",
        "ab",
        "abcd",
        " ",
        "\x00",
        "\n",
        "aa",
        "aba",
        "é",
        "e\u0301",
        "🙂",
        "🙂x",
        "a\x00b\n",
        "The quick brown fox",
        "x" * 256,
    ]

    exhaustive_alphabet = ["a", "Z", "\x00", "🙂"]
    exhaustive = [
        "".join(chars)
        for length in range(0, 6)
        for chars in itertools.product(exhaustive_alphabet, repeat=length)
    ]

    rng = random.Random(14002026)
    random_alphabet = [
        "a",
        "b",
        "Z",
        "0",
        " ",
        "\x00",
        "\n",
        "é",
        "\u0301",
        "λ",
        "🙂",
    ]
    generated = [
        "".join(rng.choice(random_alphabet) for _ in range(rng.randint(0, 96)))
        for _ in range(2000)
    ]

    cases: list[str] = []
    seen: set[str] = set()
    for case in documented_and_boundaries + exhaustive + generated:
        if case not in seen:
            seen.add(case)
            cases.append(case)

    INPUT_DUMP.write_text(
        json.dumps(
            {
                "fixed": documented_and_boundaries,
                "exhaustive_alphabet": exhaustive_alphabet,
                "exhaustive_lengths": [0, 1, 2, 3, 4, 5],
                "random_seed": 14002026,
                "random_count": 2000,
                "random_length_inclusive": [0, 96],
                "random_alphabet": random_alphabet,
                "deduplicated_cases": cases,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches: list[dict[str, object]] = []
    for value in cases:
        expected = canonical(value)
        actual = candidate(value)
        property_result = independent_oracle(value)
        if actual != expected or actual != property_result:
            mismatches.append(
                {
                    "input": value,
                    "canonical": expected,
                    "candidate": actual,
                    "independent_oracle": property_result,
                }
            )
            if len(mismatches) >= 20:
                break

    digest = hashlib.sha256(
        json.dumps(cases, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()
    lengths = sorted({len(value) for value in cases})
    print("oracle=trusted canonical.py plus independently written slicing formula")
    print(f"documented_and_fixed_count={len(documented_and_boundaries)}")
    print(
        "branch_boundaries=len 0 (zero loop iterations), "
        "len 1 (one), len >=2 (repeated)"
    )
    print(
        f"exhaustive_scope=alphabet_size_{len(exhaustive_alphabet)} "
        "lengths_0_through_5"
    )
    print(
        "generated_scope=seed_14002026 count_2000 "
        "lengths_0_through_96 unicode_and_control_alphabet"
    )
    print(f"deduplicated_case_count={len(cases)}")
    print(f"covered_lengths_min={min(lengths)} max={max(lengths)}")
    print(f"ordered_input_digest_sha256={digest}")
    print(f"input_dump={INPUT_DUMP}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, ensure_ascii=False, indent=2))
        return 1
    print("DIFFERENTIAL_TEST=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
