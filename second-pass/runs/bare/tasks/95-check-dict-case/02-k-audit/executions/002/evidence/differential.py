#!/usr/bin/env python3
"""Independent differential/contract check for HumanEval 95.

The deterministic generated corpus is the complete set of ordered, distinct
key selections of lengths 0 through 3 from KEY_POOL, plus 100 seeded length-4
samples. Dictionary values are deliberately irrelevant and are all zero.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


KEY_POOL = (
    "a",
    "b",
    "A",
    "B",
    "123",
    "a-1",
    "A-1",
    "é",
    "É",
    "δ",
    "Δ",
    8,
    None,
    (1, 2),
)

NAMED_CASES = (
    ("empty", {}),
    ("prompt-lower", {"a": "apple", "b": "banana"}),
    ("prompt-mixed", {"a": "apple", "A": "banana", "B": "banana"}),
    ("prompt-non-string", {"a": "apple", 8: "banana"}),
    ("prompt-title", {"Name": "John", "Age": "36", "City": "Houston"}),
    ("prompt-upper", {"STATE": "NC", "ZIP": "12345"}),
    ("uncased-only", {"123": 0}),
    ("lower-with-uncased", {"a-1": 0, "z9": 0}),
    ("upper-with-uncased", {"A-1": 0, "Z9": 0}),
    ("non-string-first", {8: 0, "a": 0}),
    ("non-string-middle", {"a": 0, 8: 0, "b": 0}),
    ("non-string-last", {"a": 0, "b": 0, 8: 0}),
    ("late-mixed-lower-first", {"a": 0, "b": 0, "C": 0}),
    ("late-mixed-upper-first", {"A": 0, "B": 0, "c": 0}),
    ("unicode-lower", {"é": 0, "δ": 0}),
    ("unicode-upper", {"É": 0, "Δ": 0}),
    ("unicode-mixed", {"é": 0, "Δ": 0}),
)


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def source_contract(value: dict) -> bool:
    """Direct reading of prompt.py using CPython's own string predicates."""
    if not value:
        return False
    keys = tuple(value)
    return all(isinstance(k, str) for k in keys) and (
        all(k.islower() for k in keys) or all(k.isupper() for k in keys)
    )


def outcome(function, value):
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as error:  # retained as differential evidence
        return {"kind": "raise", "value": f"{type(error).__name__}: {error}"}


def rendered_keys(value: dict) -> list[str]:
    return [repr(key) for key in value]


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential.py CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 2
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "generated_solution")

    corpus: list[tuple[str, dict]] = list(NAMED_CASES)
    for length in range(4):
        for index, keys in enumerate(itertools.permutations(KEY_POOL, length)):
            corpus.append((f"generated-{length}-{index}", dict.fromkeys(keys, 0)))

    randomizer = random.Random(950095)
    for index in range(100):
        keys = randomizer.sample(KEY_POOL, 4)
        corpus.append((f"seeded-4-{index}", dict.fromkeys(keys, 0)))

    seen: set[tuple[object, ...]] = set()
    unique_corpus: list[tuple[str, dict]] = []
    for label, value in corpus:
        fingerprint = tuple(value)
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_corpus.append((label, value))

    canonical_mismatches = []
    generated_mismatches = []
    pair_mismatches = []
    named_results = []
    for label, value in unique_corpus:
        expected = source_contract(value)
        canonical_result = outcome(canonical, value)
        generated_result = outcome(generated, value)
        expected_result = {"kind": "return", "value": expected}
        row = {
            "label": label,
            "keys": rendered_keys(value),
            "expected": expected_result,
            "canonical": canonical_result,
            "generated": generated_result,
        }
        if label in {item[0] for item in NAMED_CASES}:
            named_results.append(row)
        if canonical_result != expected_result:
            canonical_mismatches.append(row)
        if generated_result != expected_result:
            generated_mismatches.append(row)
        if canonical_result != generated_result:
            pair_mismatches.append(row)

    print("NAMED_RESULTS")
    for row in named_results:
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    print("SUMMARY")
    print(
        json.dumps(
            {
                "unique_inputs": len(unique_corpus),
                "canonical_vs_contract_mismatches": len(canonical_mismatches),
                "generated_vs_contract_mismatches": len(generated_mismatches),
                "canonical_vs_generated_mismatches": len(pair_mismatches),
                "first_canonical_vs_contract_mismatches": canonical_mismatches[:20],
                "first_generated_vs_contract_mismatches": generated_mismatches[:20],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not generated_mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
