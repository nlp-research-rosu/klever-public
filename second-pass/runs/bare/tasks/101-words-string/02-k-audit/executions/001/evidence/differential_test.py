#!/usr/bin/env python3
"""Independent canonical/candidate differential test for HumanEval 101."""

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
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


def literal_contract(value: str) -> list[str]:
    """Split only on the two delimiters named in the prompt."""
    words: list[str] = []
    current: list[str] = []
    for character in value:
        if character == "," or character == " ":
            if current:
                words.append("".join(current))
                current = []
        else:
            current.append(character)
    if current:
        words.append("".join(current))
    return words


def generated_cases() -> list[str]:
    documented_and_boundaries = [
        "Hi, my name is John",
        "One, two, three, four, five, six",
        "",
        "a",
        " ",
        ",",
        "  ",
        ",,",
        " ,",
        ", ",
        "a ",
        "a,",
        " a",
        ",a",
        "a b",
        "a,b",
        "a,,b",
        "a  b",
        "a, ,b",
        "  alpha,,beta   gamma, ",
        "word-with-punctuation,naïve café",
        "0, 1  2",
    ]

    # Exhaustively crosses empty/non-empty input, delimiter-at-index-zero,
    # no-delimiter, delimiter-after-word, and repeated/edge-delimiter paths.
    exhaustive = [
        "".join(chars)
        for length in range(0, 8)
        for chars in itertools.product("ab, ", repeat=length)
    ]

    # Deterministic broader samples contain only the separator alphabet from
    # the prompt; word characters include Unicode and punctuation.
    rng = random.Random(101)
    word_alphabet = "abcXYZ019-_éΩ"
    separators = [",", " ", ", ", ",,", "  ", " , "]
    random_cases: list[str] = []
    for _ in range(5000):
        number_of_words = rng.randrange(0, 8)
        words = [
            "".join(rng.choice(word_alphabet) for _ in range(rng.randrange(1, 13)))
            for _ in range(number_of_words)
        ]
        value = ""
        if words:
            value = words[0]
            for word in words[1:]:
                value += rng.choice(separators) + word
            if rng.randrange(2):
                value = rng.choice(separators) + value
            if rng.randrange(2):
                value += rng.choice(separators)
        random_cases.append(value)

    # Preserve order while deduplicating.
    return list(dict.fromkeys(documented_and_boundaries + exhaustive + random_cases))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    candidate = load_entry(args.candidate, "scratch_candidate")
    cases = generated_cases()

    mismatches: list[dict[str, object]] = []
    args.inputs_out.write_text(
        "".join(
            json.dumps({"index": index, "input": value}, ensure_ascii=False) + "\n"
            for index, value in enumerate(cases)
        ),
        encoding="utf-8",
    )

    for index, value in enumerate(cases):
        expected = literal_contract(value)
        canonical_result = canonical(value)
        candidate_result = candidate(value)
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": value,
                    "contract": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )

    summary = {
        "documented_examples": 2,
        "explicit_boundary_cases": 20,
        "exhaustive_alphabet": ["a", "b", ",", " "],
        "exhaustive_max_length": 7,
        "random_seed": 101,
        "random_attempts": 5000,
        "unique_cases": len(cases),
        "mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:10],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
