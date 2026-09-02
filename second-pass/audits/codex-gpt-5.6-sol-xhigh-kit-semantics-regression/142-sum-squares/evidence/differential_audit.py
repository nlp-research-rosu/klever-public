#!/usr/bin/env python3
"""Independent differential audit for HumanEval 142.

The trusted canonical and candidate-generated entry points are imported from
separate, explicit file paths. A third direct contract oracle is included so
agreement is not merely implementation-to-implementation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path

REFERENCE = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/142-sum-squares/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.jsonl")


def import_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


def contract_oracle(values: list[int]) -> int:
    total = 0
    for index, value in enumerate(values):
        if index % 3 == 0:
            total += value**2
        elif index % 4 == 0:
            total += value**3
        else:
            total += value
    return total


def named_cases():
    yield "example-1", [1, 2, 3]
    yield "example-empty", []
    yield "example-negative", [-1, -5, 2, -1, -5]

    # A unique marker at every index through 13 exercises:
    # square-only (0,3,6,9), cube-only (4,8), both-divisible precedence (12),
    # and unchanged indices. Prefixes exercise loop empty/nonempty boundaries.
    marker = [2, -3, 5, -7, 11, -13, 17, -19, 23, -29, 31, -37, 41, -43]
    for length in range(len(marker) + 1):
        yield f"prefix-{length}", marker[:length]

    # Integer magnitude/sign boundaries for the formal unbounded-Int domain.
    yield "large-positive", [10**60, -(10**45), 0, 10**30, -10**20]
    yield "large-negative", [-(10**80), 1, -1, 2, -(10**50), 3, 4, -5, 6]


def generated_cases():
    alphabet = (-3, -1, 0, 1, 2, 4)
    for length in range(6):
        for values in itertools.product(alphabet, repeat=length):
            yield f"exhaustive-{length}", list(values)

    rng = random.Random(142)
    for number in range(1000):
        length = rng.randrange(0, 41)
        values = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
        yield f"random-{number}", values


def main() -> int:
    canonical = import_entry("trusted_canonical_142", REFERENCE)
    generated = import_entry("candidate_generated_142", GENERATED)

    mismatches = []
    digest = hashlib.sha256()
    count = 0
    group_counts: dict[str, int] = {}
    with INPUT_RECORD.open("w", encoding="utf-8") as stream:
        for group, cases in (
            ("named", named_cases()),
            ("generated", generated_cases()),
        ):
            for label, values in cases:
                record = {"group": group, "label": label, "input": values}
                encoded = json.dumps(record, separators=(",", ":"), sort_keys=True)
                stream.write(encoded + "\n")
                digest.update((encoded + "\n").encode())

                expected = contract_oracle(values)
                canonical_actual = canonical(list(values))
                generated_actual = generated(list(values))
                if canonical_actual != expected or generated_actual != expected:
                    mismatches.append(
                        {
                            "label": label,
                            "input": values,
                            "oracle": expected,
                            "canonical": canonical_actual,
                            "generated": generated_actual,
                        }
                    )
                count += 1
                group_counts[group] = group_counts.get(group, 0) + 1

    print(f"REFERENCE={REFERENCE}")
    print(f"GENERATED={GENERATED}")
    print(f"INPUT_RECORD={INPUT_RECORD}")
    print(f"INPUT_SHA256={digest.hexdigest()}")
    print(f"GROUP_COUNTS={json.dumps(group_counts, sort_keys=True)}")
    print(f"TOTAL_CASES={count}")
    print(f"MISMATCHES={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:10], indent=2, sort_keys=True))
        return 1

    for label, values in named_cases():
        print(
            "CASE "
            + json.dumps(
                {
                    "label": label,
                    "input": values,
                    "result": generated(list(values)),
                },
                separators=(",", ":"),
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
