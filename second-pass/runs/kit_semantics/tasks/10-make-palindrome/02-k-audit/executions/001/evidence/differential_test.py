#!/usr/bin/env python3
"""Independent differential and contract checks for HumanEval/10."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
from types import ModuleType


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate-clean/solution.py")


def import_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_oracle(value: str) -> str:
    """Construct candidates by increasing appended-prefix length."""
    for prefix_length in range(len(value) + 1):
        answer = value + value[:prefix_length][::-1]
        if answer == answer[::-1]:
            return answer
    raise AssertionError("the complete-prefix candidate must succeed")


def first_match_index(value: str) -> int:
    expected = independent_oracle(value)
    return len(expected) - len(value)


def construct_cases() -> tuple[list[str], dict[str, int]]:
    documented = ["", "cat", "cata"]
    explicit_boundaries = [
        "a",
        "aa",
        "ab",
        "aba",
        "abba",
        "abab",
        "abca",
        "race",
        "racecar",
        "aaaaab",
        "baaaaa",
        "\x00",
        "\x00a",
        "a\x00",
        "\n\t",
        "🙂",
        "🙂a",
        "a🙂a",
        "åßç",
        "あいあ",
        "e\u0301",
        "\ud800",
        "\ud800a",
        "\U0010ffffa\U0010ffff",
    ]
    cases = documented + explicit_boundaries
    for size in range(10):
        cases.extend("".join(chars) for chars in itertools.product("ab", repeat=size))
    for size in range(8):
        cases.extend("".join(chars) for chars in itertools.product("abc", repeat=size))

    for size in (16, 31, 32, 63, 64, 127, 128, 200):
        cases.extend(
            [
                "a" * size,
                "a" * (size - 1) + "b",
                ("ab" * ((size + 1) // 2))[:size],
                ("abc" * ((size + 2) // 3))[:size],
            ]
        )

    rng = random.Random(0x10A7D17)
    alphabet = ["a", "b", "c", "X", "0", "\x00", "\n", "🙂", "å", "あ", "\u0301"]
    for _ in range(2500):
        size = rng.randrange(0, 81)
        cases.append("".join(rng.choice(alphabet) for _ in range(size)))

    # Preserve first occurrence so the exact scope is deterministic and auditable.
    cases = list(dict.fromkeys(cases))
    scope = {
        "documented": len(documented),
        "explicit_boundary_entries": len(explicit_boundaries),
        "unique_total": len(cases),
    }
    return cases, scope


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump-inputs", type=Path, required=True)
    args = parser.parse_args()

    canonical = import_path("trusted_humaneval_10", CANONICAL_PATH)
    generated = import_path("candidate_humaneval_10", GENERATED_PATH)
    cases, scope = construct_cases()

    serialized = "".join(
        json.dumps({"index": index, "input": case}, ensure_ascii=True) + "\n"
        for index, case in enumerate(cases)
    )
    args.dump_inputs.write_text(serialized, encoding="utf-8")

    mismatches: list[dict[str, object]] = []
    branch_observations = {
        "initial_found_true_cases": 0,
        "initial_found_false_cases": 0,
        "comparison_false_iterations": 0,
        "comparison_true_iterations": 0,
        "equality_at_first_prefix_cases": 0,
        "equality_at_strict_middle_cases": 0,
        "equality_at_penultimate_prefix_cases": 0,
        "post_found_guard_false_iterations": 0,
    }
    for index, case in enumerate(cases):
        reference = canonical.make_palindrome(case)
        actual = generated.make_palindrome(case)
        oracle = independent_oracle(case)
        prefix_length = first_match_index(case)
        if prefix_length == 0:
            branch_observations["initial_found_true_cases"] += 1
            branch_observations["post_found_guard_false_iterations"] += len(case)
        else:
            branch_observations["initial_found_false_cases"] += 1
            branch_observations["comparison_false_iterations"] += prefix_length - 1
            branch_observations["comparison_true_iterations"] += 1
            branch_observations["post_found_guard_false_iterations"] += (
                len(case) - prefix_length
            )
            if prefix_length == 1:
                branch_observations["equality_at_first_prefix_cases"] += 1
            if 1 < prefix_length < len(case) - 1:
                branch_observations["equality_at_strict_middle_cases"] += 1
            if prefix_length == len(case) - 1:
                branch_observations["equality_at_penultimate_prefix_cases"] += 1
        contract_ok = (
            actual.startswith(case)
            and actual == actual[::-1]
            and actual == oracle
        )
        if actual != reference or actual != oracle or not contract_ok:
            mismatches.append(
                {
                    "index": index,
                    "input": case,
                    "generated": actual,
                    "canonical": reference,
                    "oracle": oracle,
                    "contract_ok": contract_ok,
                }
            )

    print(f"canonical_path={CANONICAL_PATH}")
    print(f"generated_path={GENERATED_PATH}")
    print(f"scope={json.dumps(scope, sort_keys=True)}")
    print(f"branch_observations={json.dumps(branch_observations, sort_keys=True)}")
    print(f"input_sha256={hashlib.sha256(serialized.encode()).hexdigest()}")
    print(f"cases={len(cases)} mismatches={len(mismatches)}")
    for mismatch in mismatches[:10]:
        print(json.dumps(mismatch, ensure_ascii=True, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
