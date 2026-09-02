#!/usr/bin/env python3
"""Independent differential test for the trusted canonical and candidate entry points."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical_module = load_module(
    "audit_trusted_canonical", Path("/tmp/audit-work/canonical.py")
)
candidate_module = load_module(
    "audit_candidate_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)
canonical = canonical_module.check_if_last_char_is_a_letter
candidate = candidate_module.check_if_last_char_is_a_letter

documented = ["apple pie", "apple pi e", "apple pi e ", ""]
branch_boundaries = [
    "",
    "a",
    "A",
    "z",
    "Z",
    "0",
    "!",
    " ",
    "aa",
    " a",
    " A",
    "a ",
    "a b",
    "a B",
    "a  b",
    "a !",
]
unicode_boundaries = [
    "é",
    " é",
    "Ω",
    " Ω",
    "中",
    " 中",
    "e\u0301",
    " \u0301",
    "ß",
    " ß",
]

exhaustive_alphabet = (" ", "a", "Z", "0", "!", "é", "Ω", "\t")
exhaustive = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(exhaustive_alphabet, repeat=length)
]

rng = random.Random(134)
random_alphabet = (
    string.ascii_letters
    + string.digits
    + string.punctuation
    + " \t\n"
    + "éΩ中ß"
    + "\u0301"
)
generated = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 17)))
    for _ in range(2000)
]

tagged_inputs: list[tuple[str, str]] = []
for category, values in (
    ("documented", documented),
    ("branch_boundary", branch_boundaries),
    ("unicode_boundary", unicode_boundaries),
    ("exhaustive_len_0_through_4", exhaustive),
    ("deterministic_random", generated),
):
    tagged_inputs.extend((category, value) for value in values)

seen: set[str] = set()
unique_inputs: list[tuple[str, str]] = []
for category, value in tagged_inputs:
    if value not in seen:
        seen.add(value)
        unique_inputs.append((category, value))

mismatches: list[tuple[str, str, object, object]] = []
category_counts: dict[str, int] = {}
for category, value in unique_inputs:
    category_counts[category] = category_counts.get(category, 0) + 1
    canonical_result = canonical(value)
    candidate_result = candidate(value)
    if canonical_result != candidate_result:
        mismatches.append((category, value, canonical_result, candidate_result))

print(f"python={sys.version.split()[0]}")
print(f"unique_inputs={len(unique_inputs)}")
for category, count in category_counts.items():
    print(f"category[{category}]={count}")
print(f"mismatch_count={len(mismatches)}")
for index, (category, value, expected, actual) in enumerate(mismatches[:40], start=1):
    print(
        f"mismatch[{index}] category={category} input={value!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )
if len(mismatches) > 40:
    print(f"mismatches_omitted={len(mismatches) - 40}")

raise SystemExit(1 if mismatches else 0)
