#!/usr/bin/env python3
"""Independent differential test for HumanEval 42 (incr_list)."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from copy import deepcopy
from pathlib import Path


TRUSTED_CANONICAL = Path("/reference/canonical.py")
GENERATED_SOLUTION = Path("/tmp/audit-work/reconstruction/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.json")
RESULTS_PATH = Path("/audit-output/evidence/differential-results.json")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.incr_list


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = [
        {"class": "documented", "input": [1, 2, 3]},
        {
            "class": "documented",
            "input": [5, 3, 5, 2, 3, 3, 9, 0, 123],
        },
        {"class": "empty-loop-boundary", "input": []},
        {"class": "one-iteration-boundary", "input": [0]},
        {"class": "one-iteration-negative", "input": [-1]},
        {"class": "one-iteration-positive", "input": [1]},
        {"class": "two-iteration-boundary", "input": [-1, 0]},
        {"class": "integer-boundaries", "input": [-(10**100), -2, -1, 0, 1, 10**100]},
        {"class": "repeated-values", "input": [7, 7, 7, 7]},
    ]

    # Exhaust every list of length 0..5 over a small interval. This covers the
    # loop's zero/one/many iteration boundaries and each sign boundary.
    for length in range(6):
        for values in itertools.product(range(-2, 3), repeat=length):
            cases.append({"class": "exhaustive-small", "input": list(values)})

    # Add deterministic wider samples with large-magnitude unbounded integers.
    rng = random.Random(420042)
    for _ in range(256):
        length = rng.randrange(0, 21)
        values = [rng.randrange(-(10**30), 10**30 + 1) for _ in range(length)]
        cases.append({"class": "deterministic-generated", "input": values})

    return cases


def main() -> int:
    canonical = load_entry(TRUSTED_CANONICAL, "trusted_humaneval_42")
    generated = load_entry(GENERATED_SOLUTION, "candidate_humaneval_42")
    cases = build_cases()
    INPUTS_PATH.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    results: list[dict[str, object]] = []
    mismatches = 0
    mutation_failures = 0
    for index, case in enumerate(cases):
        original = deepcopy(case["input"])
        canonical_arg = deepcopy(original)
        generated_arg = deepcopy(original)
        expected = canonical(canonical_arg)
        actual = generated(generated_arg)
        same = actual == expected
        canonical_unchanged = canonical_arg == original
        generated_unchanged = generated_arg == original
        if not same:
            mismatches += 1
        if not canonical_unchanged or not generated_unchanged:
            mutation_failures += 1
        results.append(
            {
                "index": index,
                "class": case["class"],
                "input": original,
                "canonical": expected,
                "generated": actual,
                "equal": same,
                "canonical_input_unchanged": canonical_unchanged,
                "generated_input_unchanged": generated_unchanged,
            }
        )

    RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    results_hash = hashlib.sha256(RESULTS_PATH.read_bytes()).hexdigest()
    class_counts: dict[str, int] = {}
    for case in cases:
        label = str(case["class"])
        class_counts[label] = class_counts.get(label, 0) + 1

    print(f"trusted_oracle={TRUSTED_CANONICAL}")
    print(f"generated_entry={GENERATED_SOLUTION}")
    print(f"case_count={len(cases)}")
    print(f"class_counts={json.dumps(class_counts, sort_keys=True)}")
    print(f"mismatches={mismatches}")
    print(f"input_mutation_failures={mutation_failures}")
    print(f"results_sha256={results_hash}")
    print(f"inputs_artifact={INPUTS_PATH}")
    print(f"results_artifact={RESULTS_PATH}")
    return 0 if mismatches == 0 and mutation_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
