#!/usr/bin/env python3
"""Independent differential test for HumanEval 132 over its bracket-only domain."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import random
import re
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brute_nested(value: str) -> bool:
    """Literal contract oracle: some subsequence at i<j<k<l is '[[]]'."""
    for i, j, k, ell in itertools.combinations(range(len(value)), 4):
        if (
            value[i] == "["
            and value[j] == "["
            and value[k] == "]"
            and value[ell] == "]"
        ):
            return True
    return False


SUBSEQUENCE_PATTERN = re.compile(r"\[.*\[.*\].*\]", re.DOTALL)


def regex_nested(value: str) -> bool:
    """Independent linear-time reading of the same subsequence contract."""
    return SUBSEQUENCE_PATTERN.search(value) is not None


parser = argparse.ArgumentParser()
parser.add_argument("canonical", type=Path)
parser.add_argument("generated", type=Path)
args = parser.parse_args()

canonical = load_module("trusted_canonical", args.canonical).is_nested
generated = load_module("candidate_solution", args.generated).is_nested

documented = [
    ("[[]]", True),
    ("[]]]]]]][[[[[]", False),
    ("[][]", False),
    ("[]", False),
    ("[[][]]", True),
    ("[[]][[", True),
]

# These make every state-machine branch boundary observable: empty input;
# close at states 0/1; first/second/third open; first/second/third close after
# two opens; unmatched prefixes/suffixes; and multiple separate pairs.
boundaries = [
    "",
    "[",
    "]",
    "[[",
    "[]",
    "][",
    "]]",
    "[[[",
    "[[]",
    "[[]]",
    "[[]]]",
    "[][[]",
    "[][]",
    "][[]][",
    "]]][[[",
    "[[[[]]]]",
    "]]][[[]]",
    "[[[[[]",
    "[][[[]]][]",
]

tested = 0
mismatches: list[tuple[str, bool, bool, bool]] = []


def check(value: str, expected: bool | None = None) -> None:
    global tested
    assert set(value) <= {"[", "]"}
    want = regex_nested(value) if expected is None else expected
    if len(value) <= 8:
        assert brute_nested(value) == want
    canonical_value = canonical(value)
    generated_value = generated(value)
    tested += 1
    if not (
        isinstance(canonical_value, bool)
        and isinstance(generated_value, bool)
        and canonical_value == generated_value == want
    ):
        mismatches.append((value, want, canonical_value, generated_value))


for value, expected in documented:
    check(value, expected)
for value in boundaries:
    check(value)

# Exhaust every bracket string through length 14: 32,767 ground inputs. The
# literal four-index oracle is cross-checked on all 511 strings through length
# 8; the independent regex oracle handles the entire set.
exhaustive_count = 0
for length in range(15):
    for chars in itertools.product("[]", repeat=length):
        check("".join(chars))
        exhaustive_count += 1

# Deterministic broader sampling, including long inputs well beyond the
# exhaustive region.
rng = random.Random(132)
random_count = 0
sample_lengths = [0, 1, 2, 3, 4, 5, 8, 16, 31, 32, 64, 127, 256, 512]
for _ in range(2000):
    length = rng.choice(sample_lengths)
    check("".join(rng.choice("[]") for _ in range(length)))
    random_count += 1

structured = [
    ("[" * 4096, False),
    ("]" * 4096, False),
    ("[" * 2048 + "]" * 2048, True),
    ("[]" * 2048, True),
    ("]" * 1000 + "[[" + "]" * 1000, True),
]
for value, expected in structured:
    # Avoid the combinatorial literal oracle on very long cases. The expected
    # values are obvious from the documented subsequence condition.
    canonical_value = canonical(value)
    generated_value = generated(value)
    tested += 1
    if not (
        isinstance(canonical_value, bool)
        and isinstance(generated_value, bool)
        and canonical_value == generated_value == expected
    ):
        mismatches.append((value[:80] + "...", expected, canonical_value, generated_value))

print(f"documented_examples={len(documented)}")
print(f"explicit_boundary_cases={len(boundaries)}")
print(f"exhaustive_inputs={exhaustive_count} lengths=0..14")
print(f"deterministic_random_inputs={random_count} seed=132 lengths={sample_lengths}")
print(f"structured_long_inputs={len(structured)} max_length=4096")
print(f"total_checks={tested}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for item in mismatches[:20]:
        print("MISMATCH", repr(item))
    raise SystemExit(1)
print("RESULT canonical, generated, and literal-contract oracle agree")
