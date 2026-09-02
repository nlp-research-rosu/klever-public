#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/5.

The case set is deterministic. It includes the documented cases, all list
lengths 0..5 over {-2,-1,0,1,2} crossed with seven delimiters, explicit large
integer/boundary cases, and 500 seeded generated cases.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/candidate/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module("audit_canonical", CANONICAL).intersperse
    generated = load_module("audit_generated", GENERATED).intersperse

    documented = [
        ([], 4),
        ([1, 2, 3], 4),
    ]
    explicit_boundaries = [
        ([], 0),
        ([], -1),
        ([7], -2),
        ([0], 0),
        ([1, 2], 9),
        ([0, 0], 0),
        ([-1, 0, 1], -99),
        ([2**63 - 1, -(2**63)], 2**100),
        ([10**100, -(10**100), 0], -(10**120)),
    ]

    alphabet = (-2, -1, 0, 1, 2)
    delimiters = (-7, -2, -1, 0, 1, 2, 11)
    exhaustive = [
        (list(values), delimiter)
        for length in range(6)
        for values in itertools.product(alphabet, repeat=length)
        for delimiter in delimiters
    ]

    rng = random.Random(5005)
    generated_cases = []
    for _ in range(500):
        length = rng.randrange(0, 21)
        values = [rng.randrange(-(10**9), 10**9 + 1) for _ in range(length)]
        delimiter = rng.randrange(-(10**12), 10**12 + 1)
        generated_cases.append((values, delimiter))

    cases = documented + explicit_boundaries + exhaustive + generated_cases
    encoded = json.dumps(cases, separators=(",", ":"), ensure_ascii=True).encode()
    digest = hashlib.sha256(encoded).hexdigest()

    mismatches = []
    input_mutations = []
    non_fresh_results = []
    for index, (numbers, delimiter) in enumerate(cases):
        left_input = list(numbers)
        right_input = list(numbers)
        expected = canonical(left_input, delimiter)
        actual = generated(right_input, delimiter)
        if actual != expected:
            mismatches.append((index, numbers, delimiter, expected, actual))
        if left_input != numbers or right_input != numbers:
            input_mutations.append((index, numbers, left_input, right_input))
        if expected is left_input or actual is right_input:
            non_fresh_results.append(index)

    print(f"canonical={CANONICAL}")
    print(f"generated={GENERATED}")
    print("documented_cases=2")
    print("explicit_boundary_cases=9")
    print(
        "exhaustive_cases="
        f"{len(exhaustive)} "
        "(lengths=0..5, alphabet=[-2,-1,0,1,2], "
        "delimiters=[-7,-2,-1,0,1,2,11])"
    )
    print("seeded_generated_cases=500 seed=5005 lengths=0..20")
    print(f"total_cases={len(cases)}")
    print(f"case_stream_sha256={digest}")
    print(f"mismatches={len(mismatches)}")
    print(f"input_mutations={len(input_mutations)}")
    print(f"non_fresh_results={len(non_fresh_results)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    if input_mutations:
        print(f"first_input_mutation={input_mutations[0]!r}")
    if non_fresh_results:
        print(f"first_non_fresh_result={non_fresh_results[0]}")

    return 1 if mismatches or input_mutations or non_fresh_results else 0


if __name__ == "__main__":
    raise SystemExit(main())
