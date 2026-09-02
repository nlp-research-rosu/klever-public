#!/usr/bin/env python3
"""Independent differential audit for HumanEval 152 `compare`."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/compare152/source/solution.py")
SEED = 152_20260724


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_152", CANONICAL_PATH)
generated = load_module("candidate_solution_152", GENERATED_PATH)

named_cases = [
    ("prompt_example_1", [1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]),
    ("prompt_example_2", [0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]),
    ("empty", [], []),
    ("zero_difference", [0], [0]),
    ("positive_subtraction", [2], [-1]),
    ("negative_subtraction", [-2], [1]),
    ("negative_equal", [-7], [-7]),
    ("mixed_signs", [-7, 9], [5, -4]),
    (
        "unbounded_integer_boundary",
        [10**100, -(10**100), 0],
        [-(10**100), 10**100, 0],
    ),
    # Outside the prompt's equal-length domain, but inside the stronger K claim.
    ("left_shorter", [1], [4, 5]),
    ("right_shorter", [1, 2], [4]),
    ("left_empty", [], [4]),
    ("right_empty", [4], []),
]

cases: list[tuple[str, list[int], list[int]]] = list(named_cases)

# Exhaustive small equal-length inputs through length two.
small_values = (-3, -1, 0, 1, 3)
for length in range(3):
    vectors = list(itertools.product(small_values, repeat=length))
    for game_tuple in vectors:
        for guess_tuple in vectors:
            cases.append(("exhaustive_small", list(game_tuple), list(guess_tuple)))

# Deterministic broader representative equal-length inputs.
rng = random.Random(SEED)
random_values = [
    -(10**100),
    -(2**63),
    -10_000,
    -1,
    0,
    1,
    10_000,
    2**63 - 1,
    10**100,
]
for _ in range(2000):
    length = rng.randrange(0, 21)
    game = [rng.choice(random_values + [rng.randrange(-10**12, 10**12)]) for _ in range(length)]
    guess = [rng.choice(random_values + [rng.randrange(-10**12, 10**12)]) for _ in range(length)]
    cases.append(("deterministic_random", game, guess))

input_digest = hashlib.sha256()
mismatches = []
named_results = []
for index, (label, game, guess) in enumerate(cases):
    input_digest.update(
        json.dumps([label, game, guess], separators=(",", ":")).encode("utf-8")
    )
    expected = canonical.compare(game, guess)
    actual = generated.compare(game, guess)
    if index < len(named_cases):
        named_results.append(
            {
                "label": label,
                "game": game,
                "guess": guess,
                "canonical": expected,
                "generated": actual,
            }
        )
    if actual != expected:
        mismatches.append(
            {
                "index": index,
                "label": label,
                "game": game,
                "guess": guess,
                "canonical": expected,
                "generated": actual,
            }
        )

summary = {
    "canonical_path": str(CANONICAL_PATH),
    "generated_path": str(GENERATED_PATH),
    "seed": SEED,
    "named_results": named_results,
    "exhaustive_small_scope": {
        "integer_values": list(small_values),
        "equal_lengths": [0, 1, 2],
        "case_count": 651,
    },
    "deterministic_random_scope": {
        "case_count": 2000,
        "equal_lengths": [0, 20],
        "value_pool_includes": random_values,
        "additional_value_interval": [-10**12, 10**12 - 1],
    },
    "total_case_count": len(cases),
    "serialized_input_sha256": input_digest.hexdigest(),
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches[:10],
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
