#!/usr/bin/env python3
"""Independent differential audit for HumanEval 113 odd_count."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []

    def add(category: str, value: list[str]) -> None:
        cases.append({"category": category, "input": value})

    add("documented-example", ["1234567"])
    add("documented-example", ["3", "11111111"])
    add("outer-loop-empty", [])
    add("inner-string-empty", [""])
    add("all-single-digit-boundaries", list("0123456789"))
    add("all-even", ["02468", "000222444666888"])
    add("all-odd", ["13579", "111333555777999"])
    add("mixed-and-order", ["", "0", "1", "2468", "13579", "909090"])
    for length in [8, 9, 10, 11, 99, 100]:
        add(f"count-format-boundary-{length}", ["1" * length])

    # Exhaust every string through length four. This reaches zero/nonzero
    # recursive branches for every decimal digit and every odd-digit method.
    digits = "0123456789"
    for length in range(5):
        for chars in itertools.product(digits, repeat=length):
            add(f"exhaustive-string-length-{length}", ["".join(chars)])

    rng = random.Random(20260723)
    for _ in range(300):
        value = [
            "".join(rng.choice(digits) for _ in range(rng.randrange(0, 81)))
            for _ in range(rng.randrange(0, 10))
        ]
        add("deterministic-generated-list", value)
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True, type=Path)
    parser.add_argument("--generated", required=True, type=Path)
    parser.add_argument("--inputs", required=True, type=Path)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", args.canonical)
    generated = load_module("audited_generated", args.generated)
    cases = build_cases()
    args.inputs.write_text(json.dumps(cases, indent=2) + "\n")

    mismatches: list[dict[str, object]] = []
    category_counts: dict[str, int] = {}
    for index, case in enumerate(cases):
        category = str(case["category"])
        value = case["input"]
        category_counts[category] = category_counts.get(category, 0) + 1
        expected = canonical.odd_count(value)
        actual = generated.odd_count(value)
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "category": category,
                    "input": value,
                    "canonical": expected,
                    "generated": actual,
                }
            )
            if len(mismatches) >= 20:
                break

    print(f"cases={len(cases)}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2))
        return 1
    print("RESULT: all generated results equal the trusted canonical results")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
