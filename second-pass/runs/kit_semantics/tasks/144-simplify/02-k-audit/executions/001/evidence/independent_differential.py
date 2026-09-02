#!/usr/bin/env python3
"""Independent differential/contract check for HumanEval 144."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/144-simplify")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical")
generated = load_function(SCRATCH / "solution.py", "generated_solution")


def exact_contract(x: str, n: str) -> bool:
    a_text, b_text = x.split("/")
    c_text, d_text = n.split("/")
    a, b, c, d = map(int, (a_text, b_text, c_text, d_text))
    assert min(a, b, c, d) > 0
    return (a * c) % (b * d) == 0


def outcome(function, x: str, n: str):
    try:
        return ("value", function(x, n))
    except Exception as error:  # Boundary diagnostics intentionally retain type.
        return ("exception", type(error).__name__)


named_valid = [
    ("example_true", "1/5", "5/1"),
    ("example_false_1", "1/6", "2/1"),
    ("example_false_2", "7/10", "10/2"),
    ("unit", "1/1", "1/1"),
    ("all_parser_branches_true", "12/3", "10/4"),
    ("all_parser_branches_false", "12/7", "10/4"),
    ("leading_zeroes", "00012/00003", "00010/00004"),
    (
        "binary64_rounding_boundary",
        "9007199254740993/9007199254740992",
        "1/1",
    ),
    ("large_exact_true", "1" + "0" * 400 + "/1", "1/1"),
    ("large_exact_false", "1" + "0" * 400 + "1/2", "1/1"),
]

generated_contract_mismatches = []
canonical_contract_mismatches = []
generated_canonical_divergences = []
valid_count = 0


def check_valid(label: str, x: str, n: str) -> None:
    global valid_count
    valid_count += 1
    expected = ("value", exact_contract(x, n))
    got_generated = outcome(generated, x, n)
    got_canonical = outcome(canonical, x, n)
    if got_generated != expected:
        generated_contract_mismatches.append(
            (label, x, n, expected, got_generated)
        )
    if got_canonical != expected:
        canonical_contract_mismatches.append(
            (label, x, n, expected, got_canonical)
        )
    if got_generated != got_canonical:
        generated_canonical_divergences.append(
            (label, x, n, got_generated, got_canonical)
        )


for case in named_valid:
    check_valid(*case)

values = (1, 2, 3, 5, 9, 10, 11, 25)
for a, b, c, d in itertools.product(values, repeat=4):
    check_valid("cartesian", f"{a}/{b}", f"{c}/{d}")

rng = random.Random(144)
for index in range(5000):
    fields = [rng.randrange(1, 10**50) for _ in range(4)]
    rendered = [
        ("0" * rng.randrange(0, 5)) + str(value) for value in fields
    ]
    check_valid(
        f"random_{index}",
        f"{rendered[0]}/{rendered[1]}",
        f"{rendered[2]}/{rendered[3]}",
    )

invalid_boundary = [
    ("empty_both", "", ""),
    ("empty_x", "", "1/1"),
    ("missing_denominator", "1/", "1/1"),
    ("zero_numerator", "0/1", "1/1"),
    ("zero_denominator", "1/0", "1/1"),
    ("extra_separator", "1/2/3", "4/5"),
    ("nondigit", "a/1", "1/1"),
]

print(f"valid_cases={valid_count}")
print(
    "generated_contract_mismatches="
    f"{len(generated_contract_mismatches)}"
)
print(
    "canonical_contract_mismatches="
    f"{len(canonical_contract_mismatches)}"
)
print(
    "generated_canonical_divergences="
    f"{len(generated_canonical_divergences)}"
)
for row in canonical_contract_mismatches[:10]:
    print(f"CANONICAL_CONTRACT_MISMATCH {row!r}")
for row in generated_canonical_divergences[:10]:
    print(f"GENERATED_CANONICAL_DIVERGENCE {row!r}")

print("invalid/boundary outcomes:")
for label, x, n in invalid_boundary:
    print(
        f"{label}: generated={outcome(generated, x, n)!r} "
        f"canonical={outcome(canonical, x, n)!r}"
    )

status = 0 if not generated_contract_mismatches else 1
print(f"EXIT_STATUS: {status}")
raise SystemExit(status)
