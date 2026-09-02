#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/29."""

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
    return module.filter_by_prefix


oracle = load_function(
    Path("/tmp/audit-work/29-filter-by-prefix/trusted/canonical.py"),
    "trusted_canonical_29",
)
candidate = load_function(
    Path("/tmp/audit-work/29-filter-by-prefix/candidate-src/solution.py"),
    "candidate_solution_29",
)

cases: list[tuple[list[str], str, str]] = [
    ([], "a", "prompt-empty"),
    (["abc", "bcd", "cde", "array"], "a", "prompt-example"),
    ([], "", "empty-list-empty-prefix"),
    ([""], "", "empty-string-empty-prefix"),
    ([""], "a", "empty-string-nonempty-prefix"),
    (["a"], "", "empty-prefix"),
    (["a"], "a", "equal-boundary-match"),
    (["a"], "aa", "prefix-longer-boundary"),
    (["aa"], "a", "proper-prefix-match"),
    (["ba"], "a", "same-or-greater-length-nonmatch"),
    (["a", "a", "ab", "b", "a"], "a", "duplicates-and-order"),
    (["éclair", "e\u0301clair", "🙂alpha", "🙂"], "é", "unicode-composition"),
    (["éclair", "e\u0301clair", "🙂alpha", "🙂"], "🙂", "unicode-astral"),
    (["a\u0000b", "\u0000a", "ab"], "a\u0000", "embedded-nul"),
]

alphabet = ("a", "b", "é", "🙂")
string_pool = [""]
for length in range(1, 4):
    string_pool.extend("".join(chars) for chars in itertools.product(alphabet, repeat=length))

for value in string_pool:
    for prefix in string_pool:
        cases.append(([value], prefix, "exhaustive-singleton"))

rng = random.Random(290029)
for _ in range(1000):
    values = [rng.choice(string_pool) for _ in range(rng.randrange(0, 13))]
    prefix = rng.choice(string_pool)
    cases.append((values, prefix, "seeded-generated-list"))

mismatches: list[str] = []
for index, (values, prefix, label) in enumerate(cases):
    oracle_input = list(values)
    candidate_input = list(values)
    expected = oracle(oracle_input, prefix)
    actual = candidate(candidate_input, prefix)
    if actual != expected:
        mismatches.append(
            f"case={index} label={label} values={values!r} prefix={prefix!r} "
            f"expected={expected!r} actual={actual!r}"
        )
    if oracle_input != values or candidate_input != values:
        mismatches.append(
            f"case={index} label={label} input mutation: "
            f"original={values!r} oracle_after={oracle_input!r} "
            f"candidate_after={candidate_input!r}"
        )

print(f"documented_and_boundary_cases=14")
print(f"exhaustive_singleton_cases={len(string_pool) ** 2}")
print("seeded_generated_list_cases=1000 seed=290029 max_list_length=12")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(mismatch)
raise SystemExit(1 if mismatches else 0)
