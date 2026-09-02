#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 116."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/116-sort-array")
INPUT_RECORD = Path("/audit-output/evidence/stage2-differential-inputs.jsonl")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mathematical_oracle(values: list[int]) -> list[int]:
    # One direct lexicographic sort, independent of both two-pass implementations.
    return sorted(values, key=lambda value: (abs(value).bit_count(), value))


def generated_cases():
    explicit = [
        [],
        [0],
        [-1],
        [1],
        [-2],
        [2],
        [1, 5, 2, 3, 4],
        [-2, -3, -4, -5, -6],
        [1, 0, 2, 3, 4],
        [3, 4],
        [4, 3],
        [0, -1, 1, -2, 2, -3, 3, -4, 4],
        [7, 7, 3, 3, 1, 1, 0],
        [-(2**128), -(2**128) + 1, -1, 0, 1, 2**128 - 1, 2**128],
        [2**1024, -(2**1024), 2**1024 - 1, -(2**1024 - 1)],
    ]
    for case in explicit:
        yield "explicit", case

    alphabet = (-3, -2, -1, 0, 1, 2, 3)
    for length in range(6):
        for values in itertools.product(alphabet, repeat=length):
            yield "exhaustive_small", list(values)

    rng = random.Random(116_2026_07_29)
    boundary_pool = [
        -(2**256),
        -(2**128),
        -(2**64),
        -(2**63),
        -(2**31),
        -1025,
        -1024,
        -1023,
        -2,
        -1,
        0,
        1,
        2,
        1023,
        1024,
        1025,
        2**31 - 1,
        2**63 - 1,
        2**64,
        2**128,
        2**256,
    ]
    for _ in range(5_000):
        length = rng.randrange(0, 31)
        values = []
        for _ in range(length):
            if rng.randrange(4) == 0:
                values.append(rng.choice(boundary_pool))
            else:
                values.append(rng.randrange(-(10**18), 10**18 + 1))
        yield "random", values


def main() -> int:
    canonical_module = load_module("trusted_canonical_116", SCRATCH / "canonical.py")
    candidate_module = load_module("candidate_solution_116", SCRATCH / "solution.py")
    canonical = canonical_module.sort_array
    candidate = candidate_module.sort_array

    displayed_examples = [
        ([1, 5, 2, 3, 4], [1, 2, 3, 4, 5]),
        ([-2, -3, -4, -5, -6], [-6, -5, -4, -3, -2]),
        ([1, 0, 2, 3, 4], [0, 1, 2, 3, 4]),
    ]
    for index, (values, displayed) in enumerate(displayed_examples, 1):
        trusted = canonical(list(values))
        actual = candidate(list(values))
        print(
            f"DOCUMENTED_EXAMPLE_{index} input={values!r} "
            f"displayed={displayed!r} canonical={trusted!r} candidate={actual!r} "
            f"displayed_matches_canonical={displayed == trusted}"
        )

    counts: dict[str, int] = {}
    mismatches = 0
    mutated_inputs = 0
    aliased_outputs = 0
    record_hash = hashlib.sha256()
    total = 0
    with INPUT_RECORD.open("w", encoding="utf-8") as records:
        for source, values in generated_cases():
            total += 1
            counts[source] = counts.get(source, 0) + 1
            original = list(values)
            canonical_input = list(values)
            candidate_input = list(values)
            trusted = canonical(canonical_input)
            actual = candidate(candidate_input)
            oracle = mathematical_oracle(list(values))

            if canonical_input != original or candidate_input != original:
                mutated_inputs += 1
            if trusted is canonical_input or actual is candidate_input:
                aliased_outputs += 1
            equal = actual == trusted == oracle
            if not equal:
                mismatches += 1

            record = {
                "index": total,
                "source": source,
                "input": original,
                "canonical": trusted,
                "candidate": actual,
                "mathematical_oracle": oracle,
                "equal": equal,
            }
            serialized = json.dumps(record, sort_keys=True, separators=(",", ":"))
            records.write(serialized + "\n")
            record_hash.update((serialized + "\n").encode("utf-8"))
            if not equal:
                print(f"FIRST_MISMATCH={serialized}")
                break

    print(f"CASE_COUNTS={json.dumps(counts, sort_keys=True)}")
    print(f"TOTAL_CASES={total}")
    print(f"MISMATCHES={mismatches}")
    print(f"MUTATED_INPUTS={mutated_inputs}")
    print(f"ALIASED_OUTPUTS={aliased_outputs}")
    print(f"INPUT_RECORD={INPUT_RECORD}")
    print(f"INPUT_RECORD_SHA256={record_hash.hexdigest()}")
    return 1 if mismatches or mutated_inputs or aliased_outputs else 0


if __name__ == "__main__":
    raise SystemExit(main())
