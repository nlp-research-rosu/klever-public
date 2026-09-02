#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval 19."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from pathlib import Path
from typing import Callable


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


def load_entry(path: Path, module_name: str) -> Callable[[str], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


def outcome(function: Callable[[str], str], source: str) -> dict[str, str]:
    try:
        return {"kind": "return", "value": function(source)}
    except Exception as error:  # comparison includes exception class and message
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def intended_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    seen: set[str] = set()

    def add(source: str, tags: list[str]) -> None:
        if source not in seen:
            cases.append({"input": source, "tags": tags})
            seen.add(source)

    add("three one five", ["documented-example"])
    for source in ("", " ", "  ", "   ", "zero", "nine"):
        add(source, ["empty-or-boundary"])
    for word in WORDS:
        add(word, ["helper-branch-singleton"])
    add(" ".join(WORDS), ["ascending", "all-helper-branches"])
    add(" ".join(reversed(WORDS)), ["descending", "all-helper-branches"])
    add("nine nine zero zero five five one", ["duplicates", "stability-tie"])
    add("  eight   two zero  ", ["repeated-and-edge-spaces"])
    add(" ".join(["nine", "zero"] * 500), ["long-1000-token"])

    # Exhaust every numeral sequence through length four.
    sequences: list[tuple[str, ...]] = [()]
    for length in range(1, 5):
        next_level: list[tuple[str, ...]] = [()]
        for _ in range(length):
            next_level = [prefix + (word,) for prefix in next_level for word in WORDS]
        sequences.extend(next_level)
    for sequence in sequences:
        add(" ".join(sequence), [f"exhaustive-length-{len(sequence)}"])

    # Deterministic broader samples, with only literal-space delimiters.
    generator = random.Random(19019)
    for _ in range(500):
        length = generator.randint(0, 80)
        tokens = [generator.choice(WORDS) for _ in range(length)]
        separator = " " * generator.randint(1, 4)
        source = separator.join(tokens)
        if generator.randrange(2):
            source = (" " * generator.randint(0, 3)) + source
        if generator.randrange(2):
            source = source + (" " * generator.randint(0, 3))
        add(source, ["deterministic-generated"])

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    arguments = parser.parse_args()

    canonical = load_entry(arguments.canonical, "trusted_canonical_humaneval_19")
    generated = load_entry(arguments.generated, "audited_generated_humaneval_19")
    cases = intended_cases()
    arguments.inputs_out.write_text(
        json.dumps(
            {
                "domain": (
                    "zero or more valid numeral words, delimited only by one "
                    "or more literal ASCII spaces, with optional edge spaces"
                ),
                "case_count": len(cases),
                "cases": cases,
            },
            indent=2,
            ensure_ascii=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for case in cases:
        source = str(case["input"])
        expected = outcome(canonical, source)
        actual = outcome(generated, source)
        if expected != actual:
            mismatches.append(
                {
                    "input": source,
                    "tags": case["tags"],
                    "canonical": expected,
                    "generated": actual,
                }
            )

    digest = hashlib.sha256(arguments.inputs_out.read_bytes()).hexdigest()
    print(f"DOMAIN=intended_literal_space_delimited_valid_numerals")
    print(f"CASE_COUNT={len(cases)}")
    print(f"INPUTS_SHA256={digest}")
    print(f"MISMATCH_COUNT={len(mismatches)}")
    if mismatches:
        print("FIRST_MISMATCH=" + json.dumps(mismatches[0], ensure_ascii=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
