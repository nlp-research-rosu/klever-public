#!/usr/bin/env python3
"""Independent differential test for HumanEval/158."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import string
from pathlib import Path
from typing import Callable


def load_function(module_name: str, path: Path) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_max


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "scratch_generated", Path("/tmp/audit-work/repro/solution.py")
)


def outcome(function: Callable[[list[str]], str], words: list[str]) -> dict[str, str]:
    try:
        return {"kind": "return", "value": function(list(words))}
    except Exception as error:  # Intentionally compare observable exception classes.
        return {"kind": "raise", "value": type(error).__name__}


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/differential_test.py")
    fixed_cases = [
        # Documented examples.
        ["name", "of", "string"],
        ["name", "enam", "game"],
        ["aaaaaaa", "bb", "cc"],
        # Empty/boundary cases.
        [],
        [""],
        ["", "a"],
        ["a"],
        ["a", "b"],
        # Every loop branch: greater, equal+tiebreak true/false, and smaller.
        ["a", "ab"],
        ["ba", "ab"],
        ["ab", "ba"],
        ["abc", "aa"],
        ["aa", "abc", "cba", "z"],
        # Repeated-character and Unicode/code-point probes.
        ["aaaa", "bbb", "cc"],
        ["é", "e\u0301", "zz"],
        ["😀a", "😀😀", "ab"],
        ["Ωβ", "βα", "aa"],
    ]
    alphabet = "abcde"
    pool = [
        "".join(chars)
        for length in range(0, 4)
        for chars in itertools.product(alphabet, repeat=length)
    ]
    rng = random.Random(158)
    generated_cases: list[list[str]] = []
    for _ in range(2000):
        size = rng.randint(1, min(9, len(pool)))
        generated_cases.append(rng.sample(pool, size))

    mismatches: list[dict[str, object]] = []
    for index, words in enumerate(fixed_cases + generated_cases):
        left = outcome(canonical, words)
        right = outcome(generated, words)
        if left != right:
            mismatches.append(
                {
                    "index": index,
                    "words": words,
                    "canonical": left,
                    "generated": right,
                    "fixed_case": index < len(fixed_cases),
                }
            )

    intended_mismatches = [
        mismatch for mismatch in mismatches if mismatch["words"] != []
    ]
    print(f"fixed_cases={len(fixed_cases)}")
    print(f"generated_distinct_nonempty_cases={len(generated_cases)}")
    print(f"total_cases={len(fixed_cases) + len(generated_cases)}")
    print(f"all_mismatches={len(mismatches)}")
    print(f"nonempty_mismatches={len(intended_mismatches)}")
    print("mismatch_details=" + json.dumps(mismatches, ensure_ascii=False))
    if intended_mismatches:
        raise AssertionError("unexpected mismatch on the nonempty source-contract domain")


if __name__ == "__main__":
    main()
