#!/usr/bin/env python3
"""Independent differential test for HumanEval 7.

The oracle is loaded directly from the trusted mounted canonical.py.  The
generated implementation is loaded from the scratch copy of candidate
solution.py.  Every exercised input is written as JSON Lines.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Callable, Iterable


def load_entry(path: Path, module_name: str) -> Callable[[list[str], str], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def all_strings(alphabet: str, maximum_length: int) -> list[str]:
    return [
        "".join(chars)
        for length in range(maximum_length + 1)
        for chars in itertools.product(alphabet, repeat=length)
    ]


def generated_cases() -> Iterable[tuple[str, list[str], str]]:
    values = all_strings("ab", 3)
    needles = all_strings("ab", 2)
    for list_length in range(4):
        for members in itertools.product(values, repeat=list_length):
            for needle in needles:
                yield ("exhaustive-ab", list(members), needle)

    rng = random.Random(20260724)
    alphabet = ["a", "b", "c", " ", "é", "中", "🙂"]
    for _ in range(1000):
        strings = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(13)))
            for _ in range(rng.randrange(9))
        ]
        substring = "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(6))
        )
        yield ("seeded-random", strings, substring)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-out", required=True, type=Path)
    args = parser.parse_args()

    oracle = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/run/solution.py"), "scratch_generated_solution"
    )

    curated = [
        ("documented-empty", [], "a"),
        (
            "documented-example",
            ["abc", "bacd", "cde", "array"],
            "a",
        ),
        ("empty-needle", ["", "aa", "b"], ""),
        ("empty-string-nonempty-needle", [""], "a"),
        ("prefix", ["abc", "xbc"], "a"),
        ("middle", ["abc", "acb"], "b"),
        ("suffix", ["abc", "cab"], "c"),
        ("equal", ["abc", "ab", "xabc"], "abc"),
        ("needle-longer", ["", "a", "abc"], "abcd"),
        ("no-match", ["abc", "def"], "z"),
        ("all-match-order-duplicates", ["aa", "aa", "ba", "ab"], "a"),
        ("unicode", ["café", "é", "e\u0301", "🙂x", "中🙂"], "🙂"),
    ]

    mismatches: list[dict[str, object]] = []
    count = 0
    category_counts: dict[str, int] = {}
    args.inputs_out.parent.mkdir(parents=True, exist_ok=True)
    with args.inputs_out.open("w", encoding="utf-8") as inputs_file:
        for label, strings, substring in itertools.chain(curated, generated_cases()):
            record = {
                "label": label,
                "strings": strings,
                "substring": substring,
            }
            inputs_file.write(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            )
            before_oracle = copy.deepcopy(strings)
            before_generated = copy.deepcopy(strings)
            oracle_result = oracle(before_oracle, substring)
            generated_result = generated(before_generated, substring)
            count += 1
            category_counts[label] = category_counts.get(label, 0) + 1
            if (
                oracle_result != generated_result
                or before_oracle != strings
                or before_generated != strings
            ):
                mismatches.append(
                    {
                        **record,
                        "oracle_result": oracle_result,
                        "generated_result": generated_result,
                        "oracle_input_after": before_oracle,
                        "generated_input_after": before_generated,
                    }
                )
                if len(mismatches) >= 20:
                    break

    print(f"cases={count}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print("RESULT: all generated outputs equal the trusted canonical outputs")
    print("RESULT: neither implementation mutated any tested input list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
