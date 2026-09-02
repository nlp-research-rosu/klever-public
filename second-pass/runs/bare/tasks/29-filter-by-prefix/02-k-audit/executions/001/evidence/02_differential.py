#!/usr/bin/env python3
"""Independent CPython differential test for trusted and generated entries."""

from __future__ import annotations

import copy
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
    return module.filter_by_prefix


canonical = load_entry(
    "audit_trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "audit_generated_solution", Path("/tmp/audit-work/candidate/solution.py")
)

fixed_cases = [
    ([], "a"),
    (["abc", "bcd", "cde", "array"], "a"),
    (["", "a", "aa", "b"], ""),
    (["a"], "aa"),
    (["a", "ab", "ba", "a"], "a"),
    ([""], ""),
    (["abc"], "abc"),
    (["abc"], "abcd"),
    (["abc"], "abd"),
    (["pre", "prefix", "xpre", "pre"], "pre"),
    (["é", "élan", "e\u0301lan", "😊x"], "é"),
    (["😊", "😊x", "x😊"], "😊"),
    (["a b", " a", "a\tb", "a\nb"], "a"),
    (["\x00", "\x00a", "a\x00"], "\x00"),
]

small_strings = ("", "a", "b", "aa", "ab", "ba", "é", "😊")
small_prefixes = ("", "a", "b", "aa", "ab", "é", "😊", "x")
generated_cases = []
for length in range(4):
    for values in itertools.product(small_strings, repeat=length):
        for prefix in small_prefixes:
            generated_cases.append((list(values), prefix))

rng = random.Random(290029)
random_strings = (
    "",
    "a",
    "b",
    "aa",
    "aba",
    "prefix",
    "pre fix",
    "é",
    "e\u0301",
    "😊",
    "\x00a",
)
random_cases = [
    (
        [rng.choice(random_strings) for _ in range(rng.randrange(0, 9))],
        rng.choice(random_strings),
    )
    for _ in range(2000)
]

mismatches = []
mutation_failures = []
all_cases = fixed_cases + generated_cases + random_cases
for index, (strings, prefix) in enumerate(all_cases):
    canonical_input = copy.deepcopy(strings)
    generated_input = copy.deepcopy(strings)
    expected = canonical(canonical_input, prefix)
    actual = generated(generated_input, prefix)
    if canonical_input != strings or generated_input != strings:
        mutation_failures.append((index, strings, prefix))
    if actual != expected or type(actual) is not list:
        mismatches.append((index, strings, prefix, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"fixed_cases={len(fixed_cases)}")
print(f"exhaustive_cases={len(generated_cases)}")
print("exhaustive_scope=list lengths 0..3 over 8 strings x 8 prefixes")
print(f"seeded_random_cases={len(random_cases)} seed=290029 list_lengths=0..8")
print(f"total_cases={len(all_cases)}")
print(f"mismatches={len(mismatches)}")
print(f"input_mutation_failures={len(mutation_failures)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")
for failure in mutation_failures[:20]:
    print(f"INPUT_MUTATION {failure!r}")
raise SystemExit(1 if mismatches or mutation_failures else 0)
