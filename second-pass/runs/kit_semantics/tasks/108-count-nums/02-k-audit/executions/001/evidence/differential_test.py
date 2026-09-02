#!/usr/bin/env python3
"""Independent deterministic differential test for HumanEval 108."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


sys.dont_write_bytecode = True


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_nums


def signed_digit_sum_math(number: int) -> int:
    magnitude_digits = [ord(ch) - ord("0") for ch in str(abs(number))]
    total = sum(magnitude_digits)
    if number < 0:
        total -= 2 * magnitude_digits[0]
    return total


def independent_oracle(values: list[int]) -> int:
    return sum(signed_digit_sum_math(value) > 0 for value in values)


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: differential_test.py CANONICAL.py SOLUTION.py INPUT-MANIFEST.json",
            file=sys.stderr,
        )
        return 2

    canonical_path = Path(sys.argv[1])
    solution_path = Path(sys.argv[2])
    manifest_path = Path(sys.argv[3])
    canonical = load_function("trusted_canonical_108", canonical_path)
    generated = load_function("generated_solution_108", solution_path)

    documented = [
        [],
        [-1, 11, -11],
        [1, 1, 2],
    ]
    curated = [
        [0],
        [1],
        [-1],
        [9, 10, 11, 99, 100, 101, 109],
        [-9, -10, -11, -12, -19, -20, -90, -99, -100, -101, -102, -109],
        [10**99, -(10**99), 10**99 - 1, -(10**99 - 1)],
        [-(2**4096), 2**4096, -(2**4096 - 1), 2**4096 - 1],
        [-999999999999999999, -100000000000000001, 0, 100000000000000001],
    ]
    pool = [
        -999,
        -109,
        -102,
        -101,
        -100,
        -99,
        -20,
        -12,
        -11,
        -10,
        -1,
        0,
        1,
        9,
        10,
        11,
        12,
        99,
        100,
        101,
        109,
        999,
    ]
    exhaustive_max_length = 3
    exhaustive = [
        list(values)
        for length in range(exhaustive_max_length + 1)
        for values in itertools.product(pool, repeat=length)
    ]

    seed = 108_202_607_29
    random_count = 2_000
    rng = random.Random(seed)
    random_cases: list[list[int]] = []
    for _ in range(random_count):
        length = rng.randrange(0, 21)
        case: list[int] = []
        for _ in range(length):
            selector = rng.randrange(4)
            if selector == 0:
                case.append(rng.randrange(-10_000, 10_001))
            elif selector == 1:
                digits = rng.randrange(1, 101)
                magnitude = rng.randrange(10 ** (digits - 1), 10**digits)
                case.append(-magnitude if rng.randrange(2) else magnitude)
            elif selector == 2:
                case.append(rng.choice(pool))
            else:
                exponent = rng.randrange(0, 513)
                magnitude = 10**exponent
                delta = rng.choice([-2, -1, 0, 1, 2])
                value = magnitude + delta
                case.append(-value if rng.randrange(2) else value)

        random_cases.append(case)

    groups = [
        ("documented", documented),
        ("curated-boundaries", curated),
        ("exhaustive", exhaustive),
        ("seeded-random", random_cases),
    ]

    manifest = {
        "canonical": str(canonical_path),
        "generated": str(solution_path),
        "documented": documented,
        "curated": curated,
        "exhaustive": {
            "pool": pool,
            "lengths": list(range(exhaustive_max_length + 1)),
            "case_count": len(exhaustive),
        },
        "seeded_random": {
            "seed": seed,
            "case_count": random_count,
            "list_length_range": [0, 20],
            "integer_generation": "four selectors encoded in differential_test.py",
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    total = 0
    mismatches: list[dict[str, object]] = []
    digest = hashlib.sha256()
    for group_name, cases in groups:
        for values in cases:
            total += 1
            digest.update(json.dumps(values, separators=(",", ":")).encode())
            digest.update(b"\n")
            expected = canonical(values)
            actual = generated(values)
            independent = independent_oracle(values)
            if expected != actual or expected != independent:
                mismatches.append(
                    {
                        "group": group_name,
                        "input": values,
                        "canonical": expected,
                        "generated": actual,
                        "independent": independent,
                    }
                )
                if len(mismatches) >= 20:
                    break
        if len(mismatches) >= 20:
            break

    print(f"documented_cases={len(documented)}")
    print(f"curated_boundary_cases={len(curated)}")
    print(f"exhaustive_cases={len(exhaustive)}")
    print(f"seeded_random_cases={len(random_cases)} seed={seed}")
    print(f"total_cases={total}")
    print(f"ordered_input_sha256={digest.hexdigest()}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, sort_keys=True))
        return 1
    print("DIFFERENTIAL_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
