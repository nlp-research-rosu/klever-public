#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for HumanEval 143."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import string
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def repeated_letter(length: int, offset: int = 0) -> str:
    return string.ascii_lowercase[offset % 26] * length


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    seen: set[str] = set()

    def add(category: str, sentence: str) -> None:
        if sentence not in seen:
            cases.append(
                {
                    "id": len(cases),
                    "category": category,
                    "sentence": sentence,
                    "length": len(sentence),
                    "word_lengths": [len(word) for word in sentence.split()],
                }
            )
            seen.add(sentence)

    add("documented-example", "This is a test")
    add("documented-example", "lets go for swimming")
    add("empty-outside-contract", "")
    add("minimum-length", "a")
    add("exact-maximum-length", repeated_letter(47) + " " + repeated_letter(52, 1))
    add("all-retained", "aa bbb ccccc ggggggg")
    add("none-retained", "a bbbb cccccc dddddddd")
    add("mixed-retention", "a bb ccc dddd eeeee ffffff ggggggg")
    add("whitespace-extension", "  aa   bbb\tcccc\nccccc  ")

    # Every length comparison in the generated disjunction sees both equality
    # and non-equality cases through the complete 1..100 single-word sweep.
    for length in range(1, 101):
        add("single-word-length-1-through-100", repeated_letter(length, length))

    # Representative transitions for empty/nonempty accumulator behavior and
    # prime/composite words before and after one another.
    transition_lengths = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 97]
    for first in transition_lengths:
        for second in transition_lengths:
            sentence = repeated_letter(first, first) + " " + repeated_letter(second, second)
            if len(sentence) <= 100:
                add("two-word-branch-transition", sentence)

    randomizer = random.Random(143)
    for _ in range(750):
        word_count = randomizer.randint(1, 10)
        words: list[str] = []
        remaining = 100
        for index in range(word_count):
            separators_remaining = word_count - index - 1
            maximum = min(30, remaining - separators_remaining)
            if maximum < 1:
                break
            length = randomizer.randint(1, maximum)
            words.append(repeated_letter(length, randomizer.randrange(26)))
            remaining -= length + (1 if separators_remaining else 0)
        add("seeded-generated-valid", " ".join(words))

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    arguments = parser.parse_args()

    canonical = load_module("trusted_canonical_143", arguments.canonical)
    generated = load_module("candidate_generated_143", arguments.generated)
    cases = build_cases()
    arguments.inputs.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    results: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []
    for case in cases:
        sentence = str(case["sentence"])
        oracle_value = canonical.words_in_sentence(sentence)
        generated_value = generated.words_in_sentence(sentence)
        result = {
            "id": case["id"],
            "canonical": oracle_value,
            "generated": generated_value,
            "match": oracle_value == generated_value,
        }
        results.append(result)
        if not result["match"]:
            mismatches.append({**case, **result})

    arguments.results.write_text(
        json.dumps(
            {
                "case_count": len(cases),
                "mismatch_count": len(mismatches),
                "mismatches": mismatches,
                "results": results,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    categories = sorted({str(case["category"]) for case in cases})
    print(f"case_count={len(cases)}")
    print(f"categories={json.dumps(categories)}")
    print("single_word_lengths_covered=1..100")
    print("random_seed=143")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:10], indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
