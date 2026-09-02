#!/usr/bin/env python3
"""Differentially test trusted canonical.py and the submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "submitted_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)


def independent_oracle(text: str) -> bool:
    depth = 0
    for character in text:
        depth += 1 if character == "<" else -1
        if depth < 0:
            return False
    return depth == 0


def check(case_name: str, text: str, expected: bool | None = None) -> None:
    global checked
    reference_result = canonical(text)
    generated_result = generated(text)
    oracle_result = independent_oracle(text)
    if expected is not None and reference_result is not expected:
        raise AssertionError(
            f"{case_name}: canonical={reference_result}, expected={expected}"
        )
    if not (reference_result == generated_result == oracle_result):
        raise AssertionError(
            f"{case_name}: canonical={reference_result}, "
            f"generated={generated_result}, oracle={oracle_result}, "
            f"input={text!r}"
        )
    checked += 1


checked = 0
documented_and_boundaries = [
    ("empty", "", True),
    ("single-open", "<", False),
    ("single-close", ">", False),
    ("one-pair", "<>", True),
    ("close-before-open", "><", False),
    ("documented-nested", "<<><>>", True),
    ("documented-bad-prefix", "><<>", False),
    ("two-nested", "<<>>", True),
    ("two-sequential", "<><>", True),
    ("positive-final-depth", "<<>", False),
    ("late-negative-prefix", "<>>", False),
    ("deep-balanced", "<" * 1024 + ">" * 1024, True),
    ("deep-unclosed", "<" * 2048, False),
    ("immediate-negative-long", ">" + "<" * 2048, False),
]
for name, text, expected in documented_and_boundaries:
    check(name, text, expected)

for length in range(13):
    for characters in itertools.product("<>", repeat=length):
        check(f"exhaustive-length-{length}", "".join(characters))

rng = random.Random(560056)
for index in range(2000):
    length = rng.randrange(0, 257)
    text = "".join(rng.choice("<>") for _ in range(length))
    check(f"random-{index}", text)

print("domain=all strings over {'<','>'}")
print("exhaustive_lengths=0..12")
print("seed=560056 random_cases=2000 random_lengths=0..256")
print(f"total_cases={checked}")
print("mismatches=0")
