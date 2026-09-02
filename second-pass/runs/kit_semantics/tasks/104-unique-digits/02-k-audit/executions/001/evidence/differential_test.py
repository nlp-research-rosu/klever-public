#!/usr/bin/env python3
"""Independent differential test for HumanEval/104 on positive-integer lists."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical_104"
)
generated = load_entry(
    Path("/tmp/audit-work/candidate-src/solution.py"), "generated_solution_104"
)


def property_oracle(values: list[int]) -> list[int]:
    """Contract restatement independent of the generated numeric loop."""
    return sorted(
        value
        for value in values
        if all(digit in "13579" for digit in str(value))
    )


named_cases: list[tuple[str, list[int], list[int]]] = [
    ("prompt-1", [15, 33, 1422, 1], [1, 15, 33]),
    ("prompt-2", [152, 323, 1422, 10], []),
    ("empty", [], []),
    ("smallest-positive-keep", [1], [1]),
    ("smallest-even-drop", [2], []),
    ("while-one-iteration-keep", [9], [9]),
    ("while-one-iteration-drop", [8], []),
    ("even-first-decimal-digit", [211], []),
    ("even-middle-decimal-digit", [121], []),
    ("even-last-decimal-digit", [112], []),
    ("all-odd-multidigit", [97531], [97531]),
    ("power-boundaries", [9, 10, 11, 99, 100, 101], [9, 11, 99]),
    ("duplicates-and-sort", [97531, 1, 33, 1, 15], [1, 1, 15, 33, 97531]),
    (
        "large-values",
        [10**50 + 1, int("9" * 80), int("13579" * 30)],
        [int("9" * 80), int("13579" * 30)],
    ),
]

cases: list[tuple[str, list[int], list[int] | None]] = list(named_cases)
for value in range(1, 20_001):
    cases.append((f"singleton-{value}", [value], None))

boundary_values = [
    1,
    2,
    9,
    10,
    11,
    19,
    20,
    21,
    99,
    100,
    101,
    109,
    110,
    111,
    199,
    200,
    201,
    999,
    1000,
    1001,
    9999,
    10_000,
    10_001,
]
for left in boundary_values:
    for right in boundary_values:
        cases.append((f"boundary-pair-{left}-{right}", [left, right], None))

rng = random.Random(104_2026_07_29)
for index in range(2_000):
    length = rng.randrange(0, 25)
    values = [rng.randrange(1, 10**30) for _ in range(length)]
    cases.append((f"seeded-random-{index}", values, None))

serialized_inputs = json.dumps(
    [(name, values) for name, values, _ in cases],
    separators=(",", ":"),
    ensure_ascii=True,
).encode()
input_sha256 = hashlib.sha256(serialized_inputs).hexdigest()
print("domain=finite lists of positive Python integers")
print(
    "input-construction="
    f"named:{len(named_cases)} singleton:1..20000 "
    f"boundary-pairs:{len(boundary_values)}^2 "
    "random-seed:10420260729 random-count:2000 lengths:0..24 values:1..10^30-1"
)
print(f"case-count={len(cases)} input-json-sha256={input_sha256}")

mismatches: list[dict[str, object]] = []
for name, values, explicit_expected in cases:
    canonical_result = canonical(list(values))
    generated_result = generated(list(values))
    property_result = property_oracle(list(values))
    expected = (
        explicit_expected if explicit_expected is not None else property_result
    )
    if not (
        canonical_result
        == generated_result
        == property_result
        == expected
    ):
        mismatches.append(
            {
                "name": name,
                "input": values,
                "canonical": canonical_result,
                "generated": generated_result,
                "property": property_result,
                "expected": expected,
            }
        )
        if len(mismatches) >= 20:
            break

for name, values, explicit_expected in named_cases:
    print(
        json.dumps(
            {
                "name": name,
                "input": values,
                "canonical": canonical(list(values)),
                "generated": generated(list(values)),
                "expected": (
                    explicit_expected
                    if explicit_expected is not None
                    else property_oracle(list(values))
                ),
            },
            sort_keys=True,
        )
    )

print(f"mismatch-count={len(mismatches)}")
for mismatch in mismatches:
    print(json.dumps(mismatch, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
