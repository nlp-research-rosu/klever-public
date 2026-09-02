#!/usr/bin/env python3
"""Independent differential test for HumanEval 152 compare."""

from importlib.util import module_from_spec, spec_from_file_location
import itertools
import random


def load(path, name):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.compare


canonical = load("/reference/canonical.py", "trusted_canonical_152")
candidate = load("/tmp/audit-work/candidate/solution.py", "candidate_solution_152")

cases = [
    ("prompt-1", [1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]),
    ("prompt-2", [0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]),
    ("empty", [], []),
    ("equal-singleton", [0], [0]),
    ("positive-difference", [5], [2]),
    ("negative-difference", [2], [5]),
    ("negative-operands", [-9, -1, 0], [-4, -7, 0]),
    ("large-python-ints", [10**100, -(10**100)], [-(10**100), 10**100]),
]

alphabet = (-3, -1, 0, 1, 3)
for length in range(4):
    vectors = list(itertools.product(alphabet, repeat=length))
    for game in vectors:
        for guess in vectors:
            cases.append((f"exhaustive-len-{length}", list(game), list(guess)))

rng = random.Random(152_2026)
for index in range(10_000):
    length = rng.randrange(0, 31)
    game = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
    guess = [rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)]
    cases.append((f"random-{index}", game, guess))

mismatches = []
for label, game, guess in cases:
    expected = canonical(game, guess)
    actual = candidate(game, guess)
    if actual != expected or type(actual) is not type(expected):
        mismatches.append((label, game, guess, expected, actual))
        if len(mismatches) >= 10:
            break

print(f"cases={len(cases)}")
print("documented_examples=2")
print("exhaustive_domain=lengths 0..3 over {-3,-1,0,1,3}")
print("generated_domain=10000 seeded pairs, equal lengths 0..30, integers in [-10^12,10^12]")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", repr(mismatch))

raise SystemExit(1 if mismatches else 0)
