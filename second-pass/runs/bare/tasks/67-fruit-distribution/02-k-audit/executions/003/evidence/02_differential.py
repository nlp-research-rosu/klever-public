#!/usr/bin/env python3
"""Independent differential test against trusted canonical.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", "/reference/canonical.py")
generated = load(
    "generated_solution", "/tmp/audit-work/fruit67/candidate/solution.py"
)


def outcome(function, s, n):
    try:
        return ("return", function(s, n))
    except Exception as error:
        return ("exception", type(error).__name__, str(error))


documented = [
    ("5 apples and 6 oranges", 19),
    ("0 apples and 1 oranges", 3),
    ("2 apples and 3 oranges", 100),
    ("100 apples and 1 oranges", 120),
]
boundary_valid_format = [
    ("0 apples and 0 oranges", 0),
    ("0 apples and 0 oranges", 1),
    ("1 apples and 0 oranges", 1),
    ("0 apples and 1 oranges", 1),
    ("1 apples and 1 oranges", 2),
    ("999999 apples and 1 oranges", 1000000),
    ("0005 apples and 0006 oranges", 19),
    ("5  apples and 6 oranges", 19),
    ("  5 apples and 6 oranges  ", 19),
]

rng = random.Random(670067)
generated_valid_format = []
for _ in range(500):
    apples = rng.randrange(0, 10**6)
    oranges = rng.randrange(0, 10**6)
    mangoes = rng.randrange(0, 10**6)
    generated_valid_format.append(
        (f"{apples} apples and {oranges} oranges", apples + oranges + mangoes)
    )

# These probe behavior accepted by the trusted canonical but not explicitly
# delimited by the prose grammar. They are reported separately from the
# exact-example-format domain.
robustness = [
    ("", 10),
    ("5 apples 6 oranges", 19),
    ("basket has 5 apples and 6 oranges", 19),
    ("5 apples and 6 oranges plus 2 pears", 21),
    ("5\tapples and 6\toranges", 19),
    ("-1 apples and 2 oranges", 5),
    ("5 apples and 6 oranges and 7", 30),
]


def run_group(label, cases):
    mismatches = []
    print(f"GROUP {label} cases={len(cases)}")
    for index, (s, n) in enumerate(cases):
        left = outcome(canonical.fruit_distribution, s, n)
        right = outcome(generated.fruit_distribution, s, n)
        if left != right:
            mismatches.append((index, s, n, left, right))
    print(f"RESULT {label} mismatches={len(mismatches)}")
    for item in mismatches[:20]:
        print(f"MISMATCH {item!r}")
    return mismatches


assert not run_group("documented", documented)
assert not run_group("boundary_valid_format", boundary_valid_format)
assert not run_group("generated_valid_format_seed_670067", generated_valid_format)
robustness_mismatches = run_group("canonical_robustness_probes", robustness)
assert robustness_mismatches
print("TOTAL exact_format_cases=513 exact_format_mismatches=0")
print(f"TOTAL robustness_cases=7 robustness_mismatches={len(robustness_mismatches)}")
