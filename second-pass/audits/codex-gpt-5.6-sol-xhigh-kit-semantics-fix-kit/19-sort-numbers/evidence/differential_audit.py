#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval 19."""

from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib
import random
import sys


WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def load_entry(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


def main() -> int:
    canonical = load_entry("trusted_canonical", pathlib.Path("/reference/canonical.py"))
    candidate = load_entry("candidate_solution", pathlib.Path("/candidate/solution.py"))

    named: dict[str, str] = {
        "documented-example": "three one five",
        "empty": "",
        "one-space": " ",
        "many-spaces": "     ",
        "leading-trailing": "  nine zero  ",
        "all-ascending": " ".join(WORDS),
        "all-descending": " ".join(reversed(WORDS)),
        "duplicates": "nine zero nine zero five five",
    }
    for index, word in enumerate(WORDS):
        named[f"singleton-{index}"] = word
    for index in range(len(WORDS) - 1):
        named[f"adjacent-boundary-{index}-{index + 1}"] = (
            f"{WORDS[index + 1]} {WORDS[index]}"
        )

    cases: list[tuple[str, str]] = list(named.items())
    for length in range(5):
        for item in itertools.product(WORDS, repeat=length):
            cases.append((f"exhaustive-length-{length}", " ".join(item)))

    rng = random.Random(190719)
    for index in range(2000):
        length = rng.randrange(0, 41)
        words = [rng.choice(WORDS) for _ in range(length)]
        separators = [" " * rng.randrange(1, 5) for _ in range(max(0, length - 1))]
        text = "".join(
            piece
            for pair in itertools.zip_longest(words, separators, fillvalue="")
            for piece in pair
        )
        if rng.randrange(2):
            text = " " * rng.randrange(1, 5) + text
        if rng.randrange(2):
            text += " " * rng.randrange(1, 5)
        cases.append((f"generated-{index}", text))

    mismatches: list[dict[str, str]] = []
    for label, text in cases:
        expected = canonical(text)
        actual = candidate(text)
        if expected != actual:
            mismatches.append(
                {"label": label, "input": text, "canonical": expected, "candidate": actual}
            )
            if len(mismatches) >= 20:
                break

    print(f"documented_and_boundary_cases={len(named)}")
    for label, text in named.items():
        print(f"named_input[{label}]={text!r}")
    print("documented_example_result=" + candidate(named["documented-example"]))
    print("empty_result=" + repr(candidate(named["empty"])))
    print(f"exhaustive_sequences={sum(10 ** n for n in range(5))}")
    print("generated_cases=2000")
    print(f"total_comparisons={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
