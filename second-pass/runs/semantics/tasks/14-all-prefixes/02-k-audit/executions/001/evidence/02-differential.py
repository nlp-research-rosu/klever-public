#!/usr/bin/env python3
"""Independent differential check for HumanEval 14 all_prefixes."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.all_prefixes


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: 02-differential.py CANONICAL SOLUTION INPUTS_JSON RESULTS_JSON"
        )

    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "candidate_solution")

    documented = {
        "abc": ["a", "ab", "abc"],
        "": [],
        "a": ["a"],
    }
    for value, expected in documented.items():
        got_c = canonical(value)
        got_g = generated(value)
        if got_c != expected or got_g != expected:
            print(
                "DOCUMENTED_MISMATCH",
                repr(value),
                repr(expected),
                repr(got_c),
                repr(got_g),
            )
            return 1

    fixed = [
        "",
        "a",
        "ab",
        "abc",
        "aaaa",
        "\x00",
        "a\x00b",
        "\n",
        "é",
        "e\u0301",
        "🙂",
        "🙂x",
        "汉字",
        "a b\tc",
        "0123456789",
        "z" * 256,
    ]

    alphabet = ("a", "b", "é", "🙂")
    exhaustive = [
        "".join(chars)
        for length in range(0, 6)
        for chars in itertools.product(alphabet, repeat=length)
    ]

    rng = random.Random(140014)
    random_alphabet = ("a", "Z", "0", " ", "\x00", "\n", "é", "\u0301", "🙂", "汉")
    generated_inputs = [
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 81)))
        for _ in range(500)
    ]

    cases = []
    seen = set()
    for value in fixed + exhaustive + generated_inputs:
        if value not in seen:
            seen.add(value)
            cases.append(value)

    Path(sys.argv[3]).write_text(
        json.dumps(
            {
                "fixed": fixed,
                "exhaustive_alphabet": list(alphabet),
                "exhaustive_lengths": [0, 1, 2, 3, 4, 5],
                "random_seed": 140014,
                "random_count_requested": 500,
                "random_length_range": [0, 80],
                "random_alphabet": list(random_alphabet),
                "deduplicated_cases": cases,
            },
            ensure_ascii=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for value in cases:
        expected = canonical(value)
        actual = generated(value)
        if expected != actual:
            mismatches.append(
                {"input": value, "canonical": expected, "candidate": actual}
            )

    result = {
        "case_count": len(cases),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
    }
    Path(sys.argv[4]).write_text(
        json.dumps(result, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())

