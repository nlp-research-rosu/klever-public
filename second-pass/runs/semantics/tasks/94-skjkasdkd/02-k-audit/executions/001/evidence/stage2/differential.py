#!/usr/bin/env python3
"""Independent differential test for the trusted and generated entry points."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/reconstruction/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/stage2/differential-inputs.json")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.skjkasdkd


def mathematical_result(values: list[int]) -> int:
    """Direct oracle for the natural-language 'largest prime' contract."""

    def is_prime(value: int) -> bool:
        if value < 2:
            return False
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 1
        return True

    largest = max((value for value in values if is_prime(value)), default=0)
    return sum(int(character) for character in str(largest))


DOCUMENTED = [
    [0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3],
    [1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1],
    [1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3],
    [0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6],
    [0, 81, 12, 3, 1, 21],
    [0, 8, 1, 2, 1, 7],
]

BOUNDARIES = {
    "empty": [],
    "negative_zero_only": [-5, -1, 0],
    "one_only": [1],
    "zero_and_one": [0, 1, 0],
    "prime_cutoff_two": [2],
    "outer_equal_and_lower": [2, 2, 1],
    "outer_greater_composite_then_prime": [4, 2],
    "trial_loop_not_entered_at_three": [3],
    "trial_loop_enters_and_divides_at_four": [4],
    "trial_loop_enters_nondividing_at_five": [5],
    "later_divisor_at_nine": [9],
    "square_of_prime": [49],
    "later_larger_prime": [5, 11],
    "later_smaller_prime": [11, 5],
    "digit_zero_inside_prime": [101],
    "multi_digit_prime": [997],
    "mixed_signs_and_primes": [-7, 0, 1, 2, 17, 16],
}


def invoke(function, values):
    try:
        return ("value", function(list(values)))
    except Exception as error:  # preserve divergences in exception behavior
        return ("exception", type(error).__name__, str(error))


def main() -> int:
    canonical = load_entry(TRUSTED, "trusted_canonical")
    generated = load_entry(GENERATED, "generated_solution")

    tagged_cases: list[tuple[str, list[int]]] = []
    tagged_cases.extend((f"documented_{index + 1}", case) for index, case in enumerate(DOCUMENTED))
    tagged_cases.extend((f"boundary_{name}", case) for name, case in BOUNDARIES.items())

    alphabet = [-3, 0, 1, 2, 3, 4, 5, 9, 11, 25]
    for length in range(4):
        for values in itertools.product(alphabet, repeat=length):
            tagged_cases.append((f"exhaustive_len_{length}", list(values)))

    rng = random.Random(940094)
    for index in range(500):
        length = rng.randrange(0, 11)
        values = [rng.randrange(-50, 5001) for _ in range(length)]
        tagged_cases.append((f"generated_{index}", values))

    INPUT_RECORD.write_text(
        json.dumps(
            {
                "documented": DOCUMENTED,
                "boundaries": BOUNDARIES,
                "exhaustive_alphabet": alphabet,
                "exhaustive_lengths": [0, 1, 2, 3],
                "random_seed": 940094,
                "random_case_count": 500,
                "random_value_range": [-50, 5000],
                "random_length_range": [0, 10],
                "expanded_cases": tagged_cases,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    candidate_canonical_mismatches = []
    candidate_oracle_mismatches = []
    canonical_oracle_mismatches = []
    for label, values in tagged_cases:
        candidate_result = invoke(generated, values)
        canonical_result = invoke(canonical, values)
        oracle_result = ("value", mathematical_result(values))
        if candidate_result != canonical_result:
            candidate_canonical_mismatches.append(
                (label, values, candidate_result, canonical_result)
            )
        if candidate_result != oracle_result:
            candidate_oracle_mismatches.append(
                (label, values, candidate_result, oracle_result)
            )
        if canonical_result != oracle_result:
            canonical_oracle_mismatches.append(
                (label, values, canonical_result, oracle_result)
            )

    print(f"total_cases={len(tagged_cases)}")
    print(f"candidate_vs_canonical_mismatches={len(candidate_canonical_mismatches)}")
    print(f"candidate_vs_math_oracle_mismatches={len(candidate_oracle_mismatches)}")
    print(f"canonical_vs_math_oracle_mismatches={len(canonical_oracle_mismatches)}")
    print("first_candidate_vs_canonical_mismatches:")
    for mismatch in candidate_canonical_mismatches[:30]:
        print(repr(mismatch))
    print("first_candidate_vs_math_oracle_mismatches:")
    for mismatch in candidate_oracle_mismatches[:30]:
        print(repr(mismatch))

    # Candidate/canonical disagreements remain evidence, but the natural-
    # language oracle determines whether the generated implementation is wrong.
    return 1 if candidate_oracle_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
