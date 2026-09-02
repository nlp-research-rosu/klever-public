#!/usr/bin/env python3
"""Docstring-first differential for HumanEval 137.

The generated cases are deterministic and fully specified by VALUES and
RANDOM_SEED below. The oracle follows a defensible reading of the docstring:
strings are converted after comma-to-dot normalization, ordinary int/float
values are compared without first coercing integers to floats, and the exact
original argument is returned.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


GENERATED_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
CANONICAL_PATH = Path("/reference/canonical.py")
RANDOM_SEED = 13720260730


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


generated = load(GENERATED_PATH, "generated_solution")
canonical = load(CANONICAL_PATH, "trusted_canonical")


def numeric_value(value):
    if isinstance(value, str):
        return float(value.replace(",", "."))
    return value


def oracle(a, b):
    av = numeric_value(a)
    bv = numeric_value(b)
    if av > bv:
        return a
    if bv > av:
        return b
    return None


def outcome(function, a, b):
    try:
        result = function(a, b)
    except Exception as err:  # Edge observations include exception type.
        return ("raises", type(err).__name__, str(err))
    if result is None:
        return ("return", "None")
    if result is a:
        return ("return-original", "a", type(result).__name__, repr(result))
    if result is b:
        return ("return-original", "b", type(result).__name__, repr(result))
    return ("return-other", type(result).__name__, repr(result))


DOCUMENTED = [
    (1, 2.5),
    (1, "2,3"),
    ("5,1", "6"),
    ("1", 1),
]

# Crosses every Int/Float/str pairing and both greater branches plus equality.
VALUES = [
    -7,
    0,
    3,
    2**53,
    2**53 + 1,
    -3.5,
    -0.0,
    0.5,
    float(2**53),
    "-7",
    "-3,5",
    "0",
    "-0.0",
    "0,5",
    "3.000",
    "1e2",
]

EXPLICIT_BOUNDARIES = [
    (-1, -2),
    (-2, -1),
    (-1, -1),
    (2.0, 1),
    (1, 2.0),
    (2, 2.0),
    ("2,5", 2),
    (2, "2.5"),
    ("2.50", "2,5"),
    (2**53 + 1, float(2**53)),
    (10**400, 0.0),
]

EDGE_OBSERVATIONS = [
    ("", 0),
    (" ", 0),
    (",", 0),
    ("1,2,3", 0),
    ("nan", 1.0),
    (float("nan"), 1.0),
    (float("inf"), 1.0),
    ("inf", 1.0),
    ("١٢", 11),  # Unicode Arabic-Indic digits accepted by CPython float().
    ("1e400", 1e308),
]


def random_value(rng: random.Random):
    choice = rng.randrange(3)
    if choice == 0:
        return rng.randint(-10**18, 10**18)
    if choice == 1:
        numerator = rng.randint(-10**8, 10**8)
        denominator = rng.choice([1, 2, 4, 5, 8, 10, 100])
        return numerator / denominator
    numerator = rng.randint(-10**8, 10**8)
    scale = rng.randrange(0, 7)
    text = f"{numerator / (10**scale):.{scale}f}"
    return text.replace(".", ",") if rng.randrange(2) else text


cases = []
cases.extend(("documented", a, b) for a, b in DOCUMENTED)
cases.extend(("boundary", a, b) for a, b in EXPLICIT_BOUNDARIES)
cases.extend(("cartesian", a, b) for a in VALUES for b in VALUES)
rng = random.Random(RANDOM_SEED)
cases.extend(("random", random_value(rng), random_value(rng)) for _ in range(600))

generated_mismatches = []
canonical_mismatches = []
generated_canonical_divergences = []
by_group: dict[str, int] = {}
for index, (group, a, b) in enumerate(cases):
    by_group[group] = by_group.get(group, 0) + 1
    expected = outcome(oracle, a, b)
    actual = outcome(generated, a, b)
    witness = outcome(canonical, a, b)
    record = (index, group, repr(a), repr(b), expected, actual, witness)
    if actual != expected:
        generated_mismatches.append(record)
    if witness != expected:
        canonical_mismatches.append(record)
    if actual != witness:
        generated_canonical_divergences.append(record)

print(f"COMMAND: python3 {Path(__file__)}")
print(f"generated={GENERATED_PATH}")
print(f"canonical={CANONICAL_PATH}")
print(f"random_seed={RANDOM_SEED}")
print(f"case_groups={by_group}")
print(f"total_contract_cases={len(cases)}")
print(f"generated_vs_oracle_mismatches={len(generated_mismatches)}")
print(f"canonical_vs_oracle_mismatches={len(canonical_mismatches)}")
print(f"generated_vs_canonical_divergences={len(generated_canonical_divergences)}")
for label, records in [
    ("GENERATED_MISMATCH", generated_mismatches),
    ("CANONICAL_MISMATCH", canonical_mismatches),
    ("GENERATED_CANONICAL_DIVERGENCE", generated_canonical_divergences),
]:
    for record in records[:30]:
        print(label, record)
    if len(records) > 30:
        print(f"{label} ... {len(records) - 30} additional records omitted")

print("EDGE_OBSERVATIONS_BEGIN")
for a, b in EDGE_OBSERVATIONS:
    print(
        repr(a),
        repr(b),
        "generated=", outcome(generated, a, b),
        "canonical=", outcome(canonical, a, b),
    )
print("EDGE_OBSERVATIONS_END")

# Every documented example and all ordinary finite generated cases must satisfy
# the independent oracle. Canonical differences are observations, not failures.
raise SystemExit(1 if generated_mismatches else 0)
