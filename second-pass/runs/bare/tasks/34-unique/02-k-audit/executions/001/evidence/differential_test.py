#!/usr/bin/env python3
"""Independent differential test for HumanEval 34 `unique`.

The trusted canonical and scratch-copied generated implementation are imported
under distinct module names.  The finite input scope intentionally covers:

* the documented example;
* empty, singleton, duplicate, negative, zero, sorted, reverse, and extreme-int
  boundaries, plus representative sortable non-integer and exceptional lists;
* both orderings of two unequal values (the insertion-sort <= / > split);
* exhaustive lists of lengths 0..6 over {-2,-1,0,1,2};
* 1,500 deterministic generated integer lists of lengths 0..30.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, argument):
    before = copy.deepcopy(argument)
    try:
        result = function(argument)
        observed = ("return", result)
    except Exception as exc:  # Compare exception class and stable argument text.
        observed = ("raise", type(exc).__name__, str(exc))
    return observed, argument == before


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical_34", args.canonical)
    generated = load_module("scratch_generated_34", args.generated)

    documented_and_boundaries = [
        [5, 3, 5, 2, 3, 3, 9, 0, 123],
        [],
        [0],
        [1, 1],
        [1, 2],
        [2, 1],
        [-1, -1, 2, 0],
        [-3, -2, -1, 0, 1, 2, 3],
        [3, 2, 1, 0, -1, -2, -3],
        [7, 7, 7, 7],
        [-(10**100), 0, 10**100, -(10**100)],
        ["b", "a", "b"],
        [True, 1, False, 0],
        [(2,), (1,), (2,)],
        [1.5, -2.0, 1.5],
        [[1], [1]],  # unhashable members: both implementations must raise
        [1, "1"],  # hashable but not mutually orderable: both must raise
    ]

    exhaustive = (
        list(items)
        for length in range(7)
        for items in itertools.product(range(-2, 3), repeat=length)
    )

    rng = random.Random(340034)
    generated_cases = [
        [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 30))]
        for _ in range(1500)
    ]

    cases = itertools.chain(documented_and_boundaries, exhaustive, generated_cases)
    mismatches = []
    mutations = []
    digest = hashlib.sha256()
    count = 0
    for index, value in enumerate(cases):
        encoded = json.dumps(value, separators=(",", ":")).encode()
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        canonical_result, canonical_unchanged = outcome(canonical.unique, copy.deepcopy(value))
        generated_result, generated_unchanged = outcome(generated.unique, copy.deepcopy(value))
        if canonical_result != generated_result:
            mismatches.append((index, value, canonical_result, generated_result))
        if not canonical_unchanged or not generated_unchanged:
            mutations.append((index, value, canonical_unchanged, generated_unchanged))
        count += 1

    print("oracle=trusted /reference/canonical.py:unique")
    print("subject=scratch copy of candidate solution.py:unique")
    print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
    print("exhaustive_scope=all integer lists length 0..6 over [-2,-1,0,1,2]")
    print("generated_scope=1500 lists; seed=340034; length 0..30; values -1000..1000")
    print(f"total_cases={count}")
    print(f"ordered_input_digest_sha256={digest.hexdigest()}")
    print(f"result_mismatches={len(mismatches)}")
    print(f"input_mutation_mismatches={len(mutations)}")
    if mismatches:
        print(f"first_result_mismatch={mismatches[0]!r}")
    if mutations:
        print(f"first_mutation_mismatch={mutations[0]!r}")
    return 1 if mismatches or mutations else 0


if __name__ == "__main__":
    raise SystemExit(main())
