#!/usr/bin/env python3
"""Independent Python differential for HumanEval 16.

The test generator does not use any K proof equation or candidate-provided
test. It imports the trusted canonical and submitted Python modules by path.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_function(args.canonical, "trusted_canonical")
    generated = load_function(args.generated, "submitted_solution")

    named_cases = [
        ("documented-xyz", "xyzXYZ"),
        ("documented-jerry", "Jerry"),
        ("empty", ""),
        ("one-lower", "a"),
        ("one-upper", "A"),
        ("one-uncased", "!"),
        ("two-distinct", "ab"),
        ("duplicate-exact", "aa"),
        ("duplicate-by-case", "aA"),
        ("all-duplicate-by-case", "aAaAaA"),
        ("digits-punctuation", "123!123!"),
        ("whitespace-control", " \t\n "),
        ("unicode-lower-simple", "Σσς"),
        ("unicode-uppercase-dotted-I-expands", "\u0130"),
        ("unicode-uppercase-dotted-I-mixed", "\u0130i\u0307"),
        ("unicode-capital-sharp-s", "\u1e9eß"),
        ("unicode-supplementary", "\U00010400\U00010428"),
        ("embedded-nul", "A\u0000a"),
    ]

    cases: list[tuple[str, str]] = list(named_cases)
    exhaustive_alphabet = ["a", "A", "b", "1", "!", "Σ"]
    for length in range(0, 6):
        for chars in itertools.product(exhaustive_alphabet, repeat=length):
            cases.append((f"exhaustive-len-{length}", "".join(chars)))

    random_alphabet = [
        "a", "A", "z", "Z", "0", "9", "!", " ", "\n", "é", "É", "Σ", "ς",
        "\u0130", "\u0307", "ß", "\u1e9e", "\U00010400", "\U00010428", "中",
    ]
    rng = random.Random(160016)
    for index in range(1000):
        length = rng.randrange(0, 33)
        value = "".join(rng.choice(random_alphabet) for _ in range(length))
        cases.append((f"seeded-random-{index}", value))

    mismatches = 0
    errors = 0
    with args.results.open("w", encoding="utf-8") as stream:
        for index, (category, value) in enumerate(cases):
            row = {"index": index, "category": category, "input": value}
            try:
                expected = canonical(value)
                actual = generated(value)
                row.update(expected=expected, actual=actual)
                if type(actual) is not type(expected) or actual != expected:
                    mismatches += 1
                    row["mismatch"] = True
            except Exception as err:  # compare unexpected execution failures visibly
                errors += 1
                row["error"] = f"{type(err).__name__}: {err}"
            stream.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")

    print(f"documented/boundary cases: {len(named_cases)}")
    print("exhaustive alphabet: " + repr(exhaustive_alphabet))
    print("exhaustive lengths: 0..5")
    print("seed: 160016")
    print("seeded generated cases: 1000, lengths 0..32")
    print(f"total comparisons: {len(cases)}")
    print(f"mismatches: {mismatches}")
    print(f"errors: {errors}")
    print(f"complete per-input results: {args.results}")
    return 1 if mismatches or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
