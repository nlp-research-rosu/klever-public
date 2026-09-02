#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module("audited_candidate", Path("/candidate/solution.py"))


def check(strings: list[str], label: str) -> None:
    global checked
    canonical_input = list(strings)
    candidate_input = list(strings)
    expected = canonical.longest(canonical_input)
    actual = candidate.longest(candidate_input)
    assert actual == expected, {
        "label": label,
        "input": strings,
        "canonical": expected,
        "candidate": actual,
    }
    assert canonical_input == strings, ("canonical mutated input", label, strings)
    assert candidate_input == strings, ("candidate mutated input", label, strings)
    checked += 1


checked = 0

documented_and_boundary_cases = [
    [],
    ["a", "b", "c"],
    ["a", "bb", "ccc"],
    [""],
    ["", ""],
    ["a", ""],
    ["", "a"],
    ["aa", "b", "cc"],
    ["a", "bb", "c"],
    ["aaa", "b", "cc"],
    ["a", "b", "ccc"],
    ["same", "size", "ties"],
    ["\0", "\n", "\t"],
    ["é", "e\u0301"],
    ["🙂", "🙂🙂", "猫猫"],
    ["x" * 1000, "y" * 999, "z" * 1000],
]
for index, value in enumerate(documented_and_boundary_cases):
    check(value, f"documented-boundary-{index}")

small_pool = ["", "a", "b", "aa", "é", "猫", "🙂"]
for size in range(6):
    for values in itertools.product(small_pool, repeat=size):
        check(list(values), f"exhaustive-pool-size-{size}")

rng = random.Random(1200260729)
alphabet = ["a", "b", "é", "猫", "🙂", "\0", "\n", "\u0301"]
for index in range(5000):
    values = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 21)))
        for _ in range(rng.randrange(0, 31))
    ]
    check(values, f"seeded-random-{index}")

print(f"PASS: {checked} candidate/canonical comparisons; 0 mismatches")
