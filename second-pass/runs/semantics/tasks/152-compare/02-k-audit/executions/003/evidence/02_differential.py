#!/usr/bin/env python3
"""Independent differential test for HumanEval 152 compare."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare


canonical = load_entry(
    "trusted_canonical_compare",
    Path("/tmp/audit-work/152-compare/trusted/canonical.py"),
)
generated = load_entry(
    "candidate_generated_compare",
    Path("/tmp/audit-work/152-compare/candidate/solution.py"),
)

named_cases = [
    (
        "prompt-example-1",
        [1, 2, 3, 4, 5, 1],
        [1, 2, 3, 4, 2, -2],
        [0, 0, 0, 0, 3, 3],
    ),
    (
        "prompt-example-2",
        [0, 5, 0, 0, 0, 4],
        [4, 1, 1, 0, 0, -2],
        [4, 4, 1, 0, 0, 6],
    ),
    ("empty", [], [], []),
    ("zero-difference", [7], [7], [0]),
    ("positive-difference", [9], [2], [7]),
    ("negative-difference", [2], [9], [7]),
    ("negative-operands", [-7, -9], [-2, -14], [5, 5]),
    (
        "arbitrary-precision",
        [10**100, -(10**120)],
        [-(10**100), 10**120],
        [2 * 10**100, 2 * 10**120],
    ),
]

checks = 0
for name, game, guess, expected in named_cases:
    canonical_result = canonical(game.copy(), guess.copy())
    generated_result = generated(game.copy(), guess.copy())
    assert canonical_result == expected, (
        name,
        "canonical",
        canonical_result,
        expected,
    )
    assert generated_result == expected, (
        name,
        "generated",
        generated_result,
        expected,
    )
    checks += 1

values = (-5, -1, 0, 1, 5)
exhaustive_equal_length_pairs = 0
for length in range(5):
    lists = list(itertools.product(values, repeat=length))
    for game_tuple in lists:
        for guess_tuple in lists:
            game = list(game_tuple)
            guess = list(guess_tuple)
            expected = [abs(score - prediction) for score, prediction in zip(game, guess)]
            canonical_result = canonical(game.copy(), guess.copy())
            generated_result = generated(game.copy(), guess.copy())
            assert canonical_result == expected
            assert generated_result == expected
            assert generated_result == canonical_result
            exhaustive_equal_length_pairs += 1
            checks += 1

rng = random.Random(152)
random_equal_length_pairs = 0
for _ in range(2000):
    length = rng.randrange(0, 41)
    game = [rng.randrange(-(10**30), 10**30) for _ in range(length)]
    guess = [rng.randrange(-(10**30), 10**30) for _ in range(length)]
    expected = [abs(score - prediction) for score, prediction in zip(game, guess)]
    canonical_result = canonical(game.copy(), guess.copy())
    generated_result = generated(game.copy(), guess.copy())
    assert canonical_result == expected
    assert generated_result == expected
    assert generated_result == canonical_result
    random_equal_length_pairs += 1
    checks += 1

unequal_length_diagnostics = [
    ([1, 2], [4]),
    ([1], [4, 7]),
    ([], [1]),
    ([1], []),
]
for game, guess in unequal_length_diagnostics:
    canonical_result = canonical(game.copy(), guess.copy())
    generated_result = generated(game.copy(), guess.copy())
    expected = [abs(score - prediction) for score, prediction in zip(game, guess)]
    assert canonical_result == expected
    assert generated_result == expected
    checks += 1

print(f"named_cases={len(named_cases)}")
print(f"exhaustive_equal_length_pairs={exhaustive_equal_length_pairs}")
print(f"random_equal_length_pairs={random_equal_length_pairs}")
print(f"unequal_length_out_of_contract_diagnostics={len(unequal_length_diagnostics)}")
print(f"total_case_checks={checks}")
print("mismatches=0")
