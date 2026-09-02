#!/usr/bin/env python3
"""Independent differential test for HumanEval 74 total_match."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[str], list[str]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


def oracle(first: list[str], second: list[str]) -> list[str]:
    """Direct statement of the natural-language selection condition."""
    if sum(map(len, first)) <= sum(map(len, second)):
        return first
    return second


def all_small_lists() -> list[list[str]]:
    pool = ["", "a", "bb", "😀", "e\u0301"]
    result: list[list[str]] = []
    for length in range(3):
        result.extend([list(items) for items in itertools.product(pool, repeat=length)])
    return result


def random_list(rng: random.Random) -> list[str]:
    fragments = ["", "a", "Z", "0", "é", "e\u0301", "😀", "\n"]
    return [
        "".join(rng.choice(fragments) for _ in range(rng.randrange(0, 7)))
        for _ in range(rng.randrange(0, 7))
    ]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []

    def add(group: str, first: list[str], second: list[str]) -> None:
        cases.append({"group": group, "first": first, "second": second})

    examples = [
        ([], []),
        (["hi", "admin"], ["hI", "Hi"]),
        (["hi", "admin"], ["hi", "hi", "admin", "project"]),
        (["hi", "admin"], ["hI", "hi", "hi"]),
        (["4"], ["1", "2", "3", "4", "5"]),
    ]
    for first, second in examples:
        add("documented-example", first, second)

    boundaries = [
        ([], [""]),
        ([""], []),
        (["a"], ["b"]),
        (["ab"], ["c"]),
        (["a"], ["bc"]),
        (["", ""], [""]),
        (["ab", "c"], ["x", "yz"]),
        (["ab", "cd"], ["xyz"]),
        (["ab"], ["x", "yz"]),
        (["😀"], ["x"]),
        (["e\u0301"], ["xy"]),
        (["é"], [""]),
        (["\n"], ["x"]),
    ]
    for first, second in boundaries:
        add("manual-boundary", first, second)

    small_lists = all_small_lists()
    for first in small_lists:
        for second in small_lists:
            add("exhaustive-small", first, second)

    rng = random.Random(740074)
    for _ in range(2000):
        add("seeded-generated", random_list(rng), random_list(rng))

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "candidate_generated")
    cases = build_cases()
    args.inputs_out.write_text(
        json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    mismatches: list[dict[str, object]] = []
    branch_counts = {"first": 0, "second": 0}
    group_counts: dict[str, int] = {}
    for index, case in enumerate(cases):
        first = case["first"]
        second = case["second"]
        assert isinstance(first, list) and isinstance(second, list)
        expected = oracle(first, second)
        canonical_value = canonical(first, second)
        generated_value = generated(first, second)
        expected_branch = "first" if expected is first else "second"
        branch_counts[expected_branch] += 1
        group = str(case["group"])
        group_counts[group] = group_counts.get(group, 0) + 1
        good = (
            canonical_value == expected
            and generated_value == expected
            and (canonical_value is first) == (expected is first)
            and (canonical_value is second) == (expected is second)
            and (generated_value is first) == (expected is first)
            and (generated_value is second) == (expected is second)
        )
        if not good:
            mismatches.append(
                {
                    "index": index,
                    "case": case,
                    "expected": expected,
                    "canonical": canonical_value,
                    "generated": generated_value,
                }
            )

    inputs_hash = hashlib.sha256(args.inputs_out.read_bytes()).hexdigest()
    print(f"cases={len(cases)}")
    print(f"groups={json.dumps(group_counts, sort_keys=True)}")
    print(f"branches={json.dumps(branch_counts, sort_keys=True)}")
    print(f"inputs_sha256={inputs_hash}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:10], ensure_ascii=False, indent=2))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
