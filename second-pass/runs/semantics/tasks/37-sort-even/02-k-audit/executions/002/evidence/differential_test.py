#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval/37."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys


SCRATCH = Path("/tmp/audit-work/37-sort-even")
RESULTS = Path("/audit-output/evidence/02-differential-results.jsonl")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def cases():
    # Prompt examples and explicit branch/boundary witnesses.
    hand = [
        [],
        [7],
        [1, 2],
        [2, 1],
        [1, 2, 3],
        [3, 2, 1],
        [5, 6, 3, 4],
        [9, -1, 3, -2, 3, -3, 0],
        [0, 0, 0, 0, 0],
        [-1, 8, -1, 7, -2, 6],
        [10**100, 3, -(10**100), 4, 0],
        [2, -9, 2, -8, 1, -7, 1, -6],
    ]
    for item in hand:
        yield "hand", item

    # Exhaustive small integer lists cover loop counts 0..2 and both suffix cases.
    alphabet = (-2, -1, 0, 1, 2)
    for length in range(0, 6):
        for values in itertools.product(alphabet, repeat=length):
            yield "exhaustive", list(values)

    # Deterministic broader lengths, duplicates, negatives, and large magnitudes.
    rng = random.Random(370037)
    for _ in range(1000):
        length = rng.randrange(0, 65)
        yield "random", [rng.randint(-10**12, 10**12) for _ in range(length)]


def main() -> int:
    canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical_37")
    generated = load_function(SCRATCH / "solution.py", "generated_solution_37")
    mismatch_count = 0
    mutation_count = 0
    count = 0
    category_counts: dict[str, int] = {}
    digest = hashlib.sha256()
    with RESULTS.open("w", encoding="utf-8") as out:
        for category, original in cases():
            count += 1
            category_counts[category] = category_counts.get(category, 0) + 1
            left_input = list(original)
            right_input = list(original)
            left = canonical(left_input)
            right = generated(right_input)
            mutated = left_input != original or right_input != original
            equal = left == right
            if mutated:
                mutation_count += 1
            if not equal:
                mismatch_count += 1
            record = {
                "case": count,
                "category": category,
                "input": original,
                "canonical": left,
                "generated": right,
                "input_mutated": mutated,
                "equal": equal,
            }
            line = json.dumps(record, sort_keys=True, separators=(",", ":"))
            out.write(line + "\n")
            digest.update((line + "\n").encode())
    print(f"cases={count}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"mismatches={mismatch_count}")
    print(f"input_mutations={mutation_count}")
    print(f"results_path={RESULTS}")
    print(f"results_sha256={digest.hexdigest()}")
    return 1 if mismatch_count or mutation_count else 0


if __name__ == "__main__":
    sys.exit(main())
