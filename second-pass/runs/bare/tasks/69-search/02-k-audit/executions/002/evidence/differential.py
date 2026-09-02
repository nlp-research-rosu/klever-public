#!/usr/bin/env python3
"""Independent differential check for HumanEval/69 over its positive-list domain."""

from collections import Counter
from itertools import product
import importlib.util
from pathlib import Path
import random
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.search


def direct_oracle(values):
    frequencies = Counter(values)
    qualifying = [value for value, count in frequencies.items() if value > 0 and count >= value]
    return max(qualifying, default=-1)


root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/audit-work/69-search")
canonical = load_entry(root / "trusted-canonical.py", "trusted_canonical_69")
generated = load_entry(root / "solution.py", "generated_solution_69")

named_cases = [
    ("prompt-1", [4, 1, 2, 2, 3, 1]),
    ("prompt-2", [1, 2, 2, 3, 3, 3, 4, 4, 4]),
    ("prompt-3", [5, 5, 4, 4, 4]),
    ("singleton-qualifies", [1]),
    ("singleton-rejected", [2]),
    ("count-equals-value", [3, 3, 3]),
    ("count-greater-than-value", [2, 2, 2]),
    ("two-qualifiers-greatest", [1, 2, 2, 3, 3, 3]),
    ("qualifier-before-lower", [4, 4, 4, 4, 2, 2]),
    ("qualifier-after-lower", [2, 2, 4, 4, 4, 4]),
    ("answer-update-false", [3, 3, 3, 1, 3]),
    ("none-qualifies", [9, 8, 7, 6]),
    ("all-ones", [1] * 20),
    ("large-valid-value", [25] * 25 + [24] * 24),
]

checked = 0
for name, values in named_cases:
    c = canonical(list(values))
    g = generated(list(values))
    o = direct_oracle(values)
    print(f"NAMED {name}: canonical={c} generated={g} oracle={o} input={values}")
    assert c == g == o
    checked += 1

try:
    empty_canonical = ("value", canonical([]))
except Exception as error:
    empty_canonical = ("exception", type(error).__name__, str(error))
try:
    empty_generated = ("value", generated([]))
except Exception as error:
    empty_generated = ("exception", type(error).__name__, str(error))
print(f"OUTSIDE_DOMAIN empty: canonical={empty_canonical} generated={empty_generated}")

exhaustive = 0
for length in range(1, 7):
    for values in product(range(1, 7), repeat=length):
        values = list(values)
        c = canonical(values)
        g = generated(values)
        o = direct_oracle(values)
        assert c == g == o, (values, c, g, o)
        exhaustive += 1

rng = random.Random(690069)
random_cases = 2000
for _ in range(random_cases):
    length = rng.randint(1, 60)
    values = [rng.randint(1, 80) for _ in range(length)]
    c = canonical(values)
    g = generated(values)
    o = direct_oracle(values)
    assert c == g == o, (values, c, g, o)

checked += exhaustive + random_cases
print(
    "SUMMARY "
    f"intended_domain_cases={checked} "
    f"exhaustive_cases={exhaustive} "
    f"random_cases={random_cases} "
    "mismatches=0"
)
