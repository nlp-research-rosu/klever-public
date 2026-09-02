#!/usr/bin/env python3
"""Independent differential test for HumanEval 152 `compare`."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/152-compare")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare


canonical = load_entry(SCRATCH / "trusted" / "canonical.py", "trusted_canonical")
generated = load_entry(SCRATCH / "solution.py", "generated_solution")

documented_and_boundary = [
    ([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]),
    ([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]),
    ([], []),
    ([0], [0]),       # zero-difference branch boundary
    ([0], [1]),       # negative raw difference
    ([1], [0]),       # positive raw difference
    ([-1], [0]),
    ([0], [-1]),
    ([-10**100, 10**100], [10**100, -10**100]),
]

small_values = range(-3, 4)
exhaustive = []
for length in range(4):
    vectors = list(itertools.product(small_values, repeat=length))
    exhaustive.extend((list(game), list(guess)) for game in vectors for guess in vectors)

rng = random.Random(152)
generated_cases = []
for _ in range(500):
    length = rng.randrange(0, 65)
    game = [rng.randint(-10**12, 10**12) for _ in range(length)]
    guess = [rng.randint(-10**12, 10**12) for _ in range(length)]
    generated_cases.append((game, guess))

cases = documented_and_boundary + exhaustive + generated_cases
mismatches = []
input_digest = hashlib.sha256()
for index, (game, guess) in enumerate(cases):
    encoded = json.dumps([game, guess], separators=(",", ":")).encode()
    input_digest.update(len(encoded).to_bytes(8, "big"))
    input_digest.update(encoded)
    expected = canonical(game, guess)
    actual = generated(game, guess)
    if actual != expected:
        mismatches.append(
            {
                "index": index,
                "game": game,
                "guess": guess,
                "canonical": expected,
                "generated": actual,
            }
        )
        if len(mismatches) >= 20:
            break

print("ORACLE: /reference/canonical.py loaded from trusted scratch copy")
print("SUBJECT: candidate solution.py loaded from scratch copy")
print("DOCUMENTED_AND_BOUNDARY_CASES:", len(documented_and_boundary))
print("EXHAUSTIVE_SCOPE: equal-length integer lists, lengths 0..3, elements -3..3")
print("EXHAUSTIVE_CASES:", len(exhaustive))
print("GENERATED_SCOPE: seed 152, 500 equal-length lists, lengths 0..64, elements +/-10^12")
print("GENERATED_CASES:", len(generated_cases))
print("TOTAL_CASES:", len(cases))
print("INPUT_STREAM_SHA256:", input_digest.hexdigest())
print("MISMATCH_COUNT:", len(mismatches))
if mismatches:
    print("FIRST_MISMATCHES:", json.dumps(mismatches, sort_keys=True))
    raise SystemExit(1)

# Explicitly document one excluded unequal-length behavior difference.
try:
    generated([1], [])
except Exception as error:
    generated_unequal = f"{type(error).__name__}: {error}"
else:
    generated_unequal = "returned normally"
print("OFF_DOMAIN_WITNESS: game=[1], guess=[]")
print("OFF_DOMAIN_CANONICAL:", canonical([1], []))
print("OFF_DOMAIN_GENERATED:", generated_unequal)
