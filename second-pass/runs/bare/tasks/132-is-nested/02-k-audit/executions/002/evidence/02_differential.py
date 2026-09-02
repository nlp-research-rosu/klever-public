#!/usr/bin/env python3
"""Independent differential test: trusted canonical versus submitted Python."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical_132")
submitted = load_function(
    Path("/tmp/audit-work/132-is-nested/solution.py"), "submitted_solution_132"
)


def direct_contract_oracle(text: str) -> bool:
    """True exactly when '[', '[', ']', ']' occur in this order."""
    state = 0
    target = "[[]]"
    for character in text:
        if character == target[state]:
            state += 1
            if state == len(target):
                return True
    return False


examples = {
    "[[]]": True,
    "[]]]]]]][[[[[]": False,
    "[][]": False,
    "[]": False,
    "[[][]]": True,
    "[[]][[": True,
}

# Includes empty input, shortest true input, each automaton state boundary,
# distracting brackets, and early-return suffixes.
handcrafted = [
    "",
    "[",
    "]",
    "[[",
    "]]",
    "[]",
    "][",
    "[[]",
    "[[[]",
    "[[]]",
    "[][]",
    "]][[]][",
    "[[[[]]]]",
    "]]][[[[]]]][[[",
    "[[]]]",
    "[[]][",
    "[[]][[",
    "[][[[]]]",
]

tested: set[str] = set()
mismatches: list[tuple[str, bool, bool, bool]] = []


def check(text: str) -> None:
    if text in tested:
        return
    tested.add(text)
    expected = canonical(text)
    actual = submitted(text)
    direct = direct_contract_oracle(text)
    if expected != actual or expected != direct:
        mismatches.append((text, expected, actual, direct))


for text, expected in examples.items():
    assert canonical(text) is expected
    check(text)
for text in handcrafted:
    check(text)

# Exhaust the full bracket-only domain through length 16: 131,071 strings.
for length in range(17):
    for characters in itertools.product("[]", repeat=length):
        check("".join(characters))

# Deterministic representative long inputs exercise unbounded-looking lengths
# without confusing finite testing with a proof.
rng = random.Random(132)
for _ in range(2_000):
    length = rng.randrange(17, 1_001)
    check("".join(rng.choice("[]") for _ in range(length)))

print(f"documented_examples={len(examples)}")
print(f"handcrafted_boundary_inputs={len(handcrafted)}")
print("exhaustive_lengths=0..16")
print("deterministic_random_seed=132 random_cases=2000 random_lengths=17..1000")
print(f"unique_inputs_tested={len(tested)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")
assert not mismatches
print("DIFFERENTIAL_OK")
