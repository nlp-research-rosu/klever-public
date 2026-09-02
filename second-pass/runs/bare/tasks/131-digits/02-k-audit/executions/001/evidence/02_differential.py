#!/usr/bin/env python3
"""Independent differential test for HumanEval 131-digits.

Oracle: /reference/canonical.py (trusted mounted implementation)
Generated entry point: /tmp/audit-work/131-digits/solution.py

The formal domain is every positive Python integer.  Zero is included only as
an explicit out-of-domain boundary that exercises the zero-iteration path.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digits


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/131-digits/solution.py"), "generated_solution"
)

documented = [1, 4, 235]
out_of_domain_boundary = [0]
branch_boundaries = [
    1, 2, 9, 10, 11, 12, 20, 22, 31, 101, 111, 135, 204, 2468,
    1000, 1001, 10203, 13579, 97531, 909090, 222222, 999999,
]
decimal_structure = (
    list(range(1, 101))
    + [10**k for k in range(1, 101)]
    + [10**k - 1 for k in range(1, 101)]
    + [int(str(d) * k) for d in range(1, 10) for k in (2, 5, 20, 100)]
)
exhaustive_small = list(range(1, 10001))

rng = random.Random(131)
generated_random = [
    rng.randrange(1, 10 ** rng.randrange(1, 101)) for _ in range(500)
]

groups = {
    "documented": documented,
    "out_of_domain_boundary": out_of_domain_boundary,
    "branch_boundaries": branch_boundaries,
    "decimal_structure": decimal_structure,
    "exhaustive_small": exhaustive_small,
    "generated_random_seed_131": generated_random,
}

print("oracle=/reference/canonical.py:digits")
print("subject=/tmp/audit-work/131-digits/solution.py:digits")
print("formal_domain=positive Python integers")
print("out_of_domain_cases=[0]")
print("generated_random_seed=131")
print(f"generated_random_values={generated_random!r}")
print("group_counts=" + repr({name: len(values) for name, values in groups.items()}))

mismatches = []
checked = 0
seen = set()
for group, values in groups.items():
    for n in values:
        key = (group, n)
        if key in seen:
            continue
        seen.add(key)
        checked += 1
        try:
            expected = ("return", canonical(n))
        except Exception as err:  # preserve exception class as observable behavior
            expected = ("raise", type(err).__name__, str(err))
        try:
            actual = ("return", generated(n))
        except Exception as err:
            actual = ("raise", type(err).__name__, str(err))
        if actual != expected:
            mismatches.append((group, n, expected, actual))

for n in documented + [0, 2, 9, 10, 11, 22, 101, 235, 2468, 10203, 13579]:
    print(
        f"sample n={n} canonical={canonical(n)!r} generated={generated(n)!r}"
    )

print(f"checks={checked}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
