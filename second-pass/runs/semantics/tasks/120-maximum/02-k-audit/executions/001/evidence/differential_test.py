#!/usr/bin/env python3
"""Independent result differential for HumanEval 120 maximum."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Callable


TRUSTED_CANONICAL = Path("/tmp/audit-work/120-maximum/trusted/canonical.py")
CANDIDATE_SOLUTION = Path(
    "/tmp/audit-work/120-maximum/candidate-source/solution.py"
)
INPUT_RECORD = Path("/audit-output/evidence/stage2-inputs.jsonl")


def load_entry(path: Path, module_name: str) -> Callable[[list[int], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "maximum")
    return entry


def expected(arr: list[int], k: int) -> list[int]:
    if k == 0:
        return []
    return sorted(arr)[len(arr) - k :]


def generate_cases() -> list[tuple[str, list[int], int]]:
    cases: list[tuple[str, list[int], int]] = [
        ("example-1", [-3, -4, 5], 3),
        ("example-2", [4, -4, 4], 2),
        ("example-3", [-3, 2, 1, 2, -1, -2, 1], 1),
        ("empty-outside-domain", [], 0),
        ("singleton-min-k0", [-1000], 0),
        ("singleton-min-k1", [-1000], 1),
        ("singleton-max-k0", [1000], 0),
        ("singleton-max-k1", [1000], 1),
        ("branch-k0", [3, 1, 2], 0),
        ("branch-k1", [3, 1, 2], 1),
        ("slice-k-n-minus-1", [3, 1, 2], 2),
        ("slice-k-n", [3, 1, 2], 3),
        ("all-duplicates", [4, 4, 4, 4], 3),
        ("mixed-extrema-k1", [-1000, 1000, 0, -1000, 1000], 1),
        ("mixed-extrema-kn", [-1000, 1000, 0, -1000, 1000], 5),
        ("max-length-k0", [(-1000 if i % 2 == 0 else 1000) for i in range(1000)], 0),
        ("max-length-k1", [(-1000 if i % 2 == 0 else 1000) for i in range(1000)], 1),
        ("max-length-kn", [(-1000 if i % 2 == 0 else 1000) for i in range(1000)], 1000),
    ]

    small_values = (-2, -1, 0, 1, 2)
    for length in range(0, 6):
        for ordinal, values in enumerate(itertools.product(small_values, repeat=length)):
            arr = list(values)
            for k in range(length + 1):
                cases.append((f"exhaustive-l{length}-a{ordinal}-k{k}", arr, k))

    rng = random.Random(120_2026_07_24)
    for index in range(256):
        length = rng.randint(1, 1000)
        arr = [rng.randint(-1000, 1000) for _ in range(length)]
        boundary_ks = [0, 1, max(0, length - 1), length]
        k = boundary_ks[index % len(boundary_ks)] if index < 128 else rng.randint(0, length)
        cases.append((f"random-{index}", arr, k))
    return cases


def main() -> int:
    canonical = load_entry(TRUSTED_CANONICAL, "trusted_canonical_120")
    candidate = load_entry(CANDIDATE_SOLUTION, "candidate_solution_120")
    cases = generate_cases()
    mismatches: list[dict[str, object]] = []
    invariant_failures: list[dict[str, object]] = []
    canonical_mutations = 0
    candidate_mutations = 0

    with INPUT_RECORD.open("w", encoding="utf-8") as stream:
        for label, arr, k in cases:
            stream.write(
                json.dumps({"label": label, "arr": arr, "k": k}, separators=(",", ":"))
                + "\n"
            )

            canonical_input = list(arr)
            candidate_input = list(arr)
            canonical_result = canonical(canonical_input, k)
            candidate_result = candidate(candidate_input, k)
            oracle_result = expected(arr, k)

            canonical_mutations += int(canonical_input != arr)
            candidate_mutations += int(candidate_input != arr)

            if canonical_result != candidate_result or candidate_result != oracle_result:
                if len(mismatches) < 20:
                    mismatches.append(
                        {
                            "label": label,
                            "arr": arr,
                            "k": k,
                            "canonical": canonical_result,
                            "candidate": candidate_result,
                            "oracle": oracle_result,
                        }
                    )

            if not (
                candidate_result == sorted(candidate_result)
                and len(candidate_result) == k
                and Counter(candidate_result) <= Counter(arr)
            ):
                if len(invariant_failures) < 20:
                    invariant_failures.append(
                        {
                            "label": label,
                            "arr": arr,
                            "k": k,
                            "candidate": candidate_result,
                        }
                    )

    print(f"trusted_canonical={TRUSTED_CANONICAL}")
    print(f"candidate_solution={CANDIDATE_SOLUTION}")
    print(f"input_record={INPUT_RECORD}")
    print("scope=3 examples + empty + extrema + all branch/slice boundaries")
    print("scope+=all arrays of lengths 0..5 over {-2,-1,0,1,2}, all valid k")
    print("scope+=256 deterministic arrays of length 1..1000, values -1000..1000")
    print(f"cases={len(cases)}")
    print(f"result_mismatches={len(mismatches)}")
    print(f"invariant_failures={len(invariant_failures)}")
    print(f"canonical_input_mutations={canonical_mutations}")
    print(f"candidate_input_mutations={candidate_mutations}")
    if mismatches:
        print(f"first_result_mismatches={json.dumps(mismatches, sort_keys=True)}")
    if invariant_failures:
        print(f"first_invariant_failures={json.dumps(invariant_failures, sort_keys=True)}")
    return 1 if mismatches or invariant_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
