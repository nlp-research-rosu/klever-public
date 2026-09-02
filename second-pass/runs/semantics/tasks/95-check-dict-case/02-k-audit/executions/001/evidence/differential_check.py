#!/usr/bin/env python3
"""Independent differential check for HumanEval 95.

The oracle and generated implementation are loaded directly from the trusted
reference mount and read-only candidate mount.  Values do not affect the
contract, so inputs focus on key types and key case classifications.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: str, module_name: str) -> Callable[[dict[Any, Any]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


canonical = load_entry("/tmp/audit-work/trusted/canonical.py", "trusted_canonical")
generated = load_entry("/tmp/audit-work/src/solution.py", "generated_solution")

documented: list[tuple[str, dict[Any, Any]]] = [
    ("example_lower", {"a": "apple", "b": "banana"}),
    ("example_mixed", {"a": "apple", "A": "banana", "B": "banana"}),
    ("example_nonstr", {"a": "apple", 8: "banana"}),
    ("example_title", {"Name": "John", "Age": "36", "City": "Houston"}),
    ("example_upper", {"STATE": "NC", "ZIP": "12345"}),
]

boundaries: list[tuple[str, dict[Any, Any]]] = [
    ("empty", {}),
    ("single_lower", {"a": 0}),
    ("single_upper", {"A": 0}),
    ("single_uncased_empty", {"": 0}),
    ("single_uncased_digits", {"123": 0}),
    ("single_mixedcase", {"aA": 0}),
    ("single_nonstr_int", {0: 0}),
    ("single_nonstr_tuple", {(1, 2): 0}),
    ("late_mixed_after_two_lower", {"a": 0, "b": 0, "A": 0}),
    ("late_nonstr_after_two_lower", {"a": 0, "b": 0, 7: 0}),
    ("late_mixed_after_two_upper", {"A": 0, "B": 0, "a": 0}),
    ("unicode_lower", {"é": 0}),
    ("unicode_upper", {"É": 0}),
]

# Exhaust every ordered sequence of up to four distinct representatives.  The
# list covers lower, upper, uncased string, mixed-case string, and non-string
# branches.  Distinct dictionary keys preserve the chosen insertion order.
representatives: list[Any] = ["a", "b", "A", "B", "123", "aA", 0, (1,)]
generated_cases: list[tuple[str, dict[Any, Any]]] = []
for length in range(5):
    for index, keys in enumerate(itertools.permutations(representatives, length)):
        generated_cases.append(
            (f"perm_{length}_{index}", {key: pos for pos, key in enumerate(keys)})
        )

# A fixed-seed broader sample includes ordinary ASCII strings, uncased strings,
# non-string keys, and Unicode cased strings.
rng = random.Random(950095)
pool: list[Any] = [
    "x",
    "xy",
    "X",
    "XY",
    "xY",
    "0",
    "-",
    "",
    "é",
    "É",
    1,
    2,
    (3,),
]
random_cases: list[tuple[str, dict[Any, Any]]] = []
for index in range(500):
    count = rng.randrange(0, 7)
    keys = rng.sample(pool, count)
    random_cases.append((f"random_{index}", {key: index for key in keys}))

cases = documented + boundaries + generated_cases + random_cases
mismatches: list[dict[str, Any]] = []
generated_contract_failures: list[dict[str, Any]] = []


def direct_contract(value: dict[Any, Any]) -> bool:
    if not value:
        return False
    keys = list(value)
    return all(isinstance(key, str) and key.islower() for key in keys) or all(
        isinstance(key, str) and key.isupper() for key in keys
    )


for name, value in cases:
    can = canonical(value)
    gen = generated(value)
    expected = direct_contract(value)
    if can != gen:
        mismatches.append(
            {
                "name": name,
                "input_repr": repr(value),
                "canonical": can,
                "generated": gen,
                "direct_contract": expected,
            }
        )
    if gen != expected:
        generated_contract_failures.append(
            {
                "name": name,
                "input_repr": repr(value),
                "generated": gen,
                "direct_contract": expected,
            }
        )

print(
    json.dumps(
        {
            "case_count": len(cases),
            "documented_count": len(documented),
            "boundary_count": len(boundaries),
            "exhaustive_permutation_count": len(generated_cases),
            "fixed_seed_random_count": len(random_cases),
            "canonical_generated_mismatch_count": len(mismatches),
            "generated_contract_failure_count": len(generated_contract_failures),
            "first_20_canonical_generated_mismatches": mismatches[:20],
            "first_20_generated_contract_failures": generated_contract_failures[:20],
        },
        indent=2,
        sort_keys=True,
    )
)

if generated_contract_failures:
    raise SystemExit(1)
