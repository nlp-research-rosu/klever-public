#!/usr/bin/env python3
"""Independent differential test for HumanEval/19 over its space-token domain."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/19-sort-numbers/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/02-differential-inputs.json")
RESULTS_PATH = Path("/audit-output/evidence/02-differential-results.json")
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


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


def main() -> int:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    candidate = load_function("audited_candidate", CANDIDATE_PATH)

    curated = [
        "three one five",
        "",
        " ",
        "   ",
        "zero",
        "nine",
        "zero nine",
        "nine zero",
        "nine eight seven six five four three two one zero",
        "zero one two three four five six seven eight nine",
        "five five five",
        "  three one five",
        "three one five  ",
        "three  one    five",
        "nine zero nine zero one",
    ]
    curated.extend(WORDS)

    exhaustive = [
        " ".join(items)
        for length in range(5)
        for items in itertools.product(WORDS, repeat=length)
    ]

    rng = random.Random(190019)
    random_cases: list[str] = []
    for _ in range(1000):
        length = rng.randrange(0, 101)
        items = [rng.choice(WORDS) for _ in range(length)]
        separator = " " * rng.randrange(1, 5)
        value = separator.join(items)
        value = (" " * rng.randrange(0, 4)) + value + (" " * rng.randrange(0, 4))
        random_cases.append(value)

    inputs = list(dict.fromkeys(curated + exhaustive + random_cases))
    serialized_inputs = json.dumps(inputs, ensure_ascii=True, indent=2) + "\n"
    INPUTS_PATH.write_text(serialized_inputs)

    mismatches = []
    for value in inputs:
        try:
            expected = ("return", canonical(value))
        except Exception as err:  # Included to compare observable exceptional behavior.
            expected = ("raise", type(err).__name__, str(err))
        try:
            actual = ("return", candidate(value))
        except Exception as err:
            actual = ("raise", type(err).__name__, str(err))
        if actual != expected:
            mismatches.append({"input": value, "canonical": expected, "candidate": actual})

    key_results = {word: candidate(word) for word in WORDS}
    results = {
        "contract_domain": "finite strings of zero or more valid numeral words separated by one or more ASCII spaces, allowing leading/trailing spaces",
        "curated_count_before_deduplication": len(curated),
        "exhaustive_scope": "all 10^n word sequences for n=0,1,2,3,4",
        "exhaustive_count_before_deduplication": len(exhaustive),
        "random_scope": "seed 190019; 1000 sequences; length 0..100; separators/leading/trailing ASCII spaces",
        "random_count_before_deduplication": len(random_cases),
        "unique_input_count": len(inputs),
        "inputs_sha256": hashlib.sha256(serialized_inputs.encode()).hexdigest(),
        "key_singletons": key_results,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
    }
    RESULTS_PATH.write_text(json.dumps(results, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(results, ensure_ascii=True, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
