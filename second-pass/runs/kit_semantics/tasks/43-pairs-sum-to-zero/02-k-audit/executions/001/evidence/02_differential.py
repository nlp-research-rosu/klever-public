#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/43."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/review-43")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


def independent_oracle(values: list[int]) -> bool:
    return any(
        values[left] + values[right] == 0
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )


def main() -> int:
    canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical_43")
    generated = load_function(SCRATCH / "solution.py", "candidate_solution_43")

    documented = [
        ([1, 3, 5, 0], False),
        ([1, 3, -2, 1], False),
        ([1, 2, 3, 7], False),
        ([2, 4, -5, 3, 5, 7], True),
        ([1], False),
    ]
    boundaries = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [1],
        [-1],
        [1, 1],
        [1, -1],
        [-1, 1],
        [1, -1, -1],
        [2, 0, -2],
        [2, 0, 3],
        [10**100, -(10**100)],
        [-(10**100), 1, 10**100],
        [10**100, 10**100],
    ]
    exhaustive = [
        list(values)
        for length in range(7)
        for values in itertools.product(range(-2, 3), repeat=length)
    ]
    rng = random.Random(430043)
    generated_cases = [
        [rng.randint(-10**40, 10**40) for _ in range(rng.randint(0, 30))]
        for _ in range(2500)
    ]
    # Deliberately seed some generated lists with inverse pairs at varied
    # positions so both result classes remain well represented.
    for index, values in enumerate(generated_cases[:1000]):
        chosen = index + 3
        values.extend([chosen, -chosen])

    cases = [values for values, _ in documented]
    cases.extend(boundaries)
    cases.extend(exhaustive)
    cases.extend(generated_cases)

    mismatches: list[tuple[list[int], bool, bool, bool]] = []
    true_count = 0
    false_count = 0
    for values in cases:
        expected = independent_oracle(values)
        reference_value = canonical(values.copy())
        generated_value = generated(values.copy())
        if expected:
            true_count += 1
        else:
            false_count += 1
        if reference_value != expected or generated_value != expected:
            mismatches.append(
                (values, expected, reference_value, generated_value)
            )
            if len(mismatches) <= 20:
                print(
                    "MISMATCH "
                    f"input={values!r} oracle={expected!r} "
                    f"canonical={reference_value!r} generated={generated_value!r}"
                )

    for values, expected in documented:
        actual = generated(values.copy())
        print(f"EXAMPLE input={values!r} expected={expected} generated={actual}")
        if actual != expected:
            mismatches.append((values, expected, canonical(values), actual))

    for values in ([], [1, -1], [0], [0, 0]):
        print(
            f"GROUND input={values!r} oracle={independent_oracle(values)} "
            f"canonical={canonical(values.copy())} "
            f"generated={generated(values.copy())}"
        )

    print(f"DOCUMENTED_CASES={len(documented)}")
    print(f"BOUNDARY_CASES={len(boundaries)}")
    print("EXHAUSTIVE_DOMAIN=lengths 0..6, values -2..2")
    print(f"EXHAUSTIVE_CASES={len(exhaustive)}")
    print("GENERATED_DOMAIN=2500 deterministic lists, lengths 0..30, unbounded ints")
    print(f"GENERATED_CASES={len(generated_cases)}")
    print(f"TOTAL_COMPARISONS={len(cases)}")
    print(f"ORACLE_TRUE={true_count}")
    print(f"ORACLE_FALSE={false_count}")
    print(f"MISMATCHES={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
