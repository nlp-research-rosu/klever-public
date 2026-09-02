#!/usr/bin/env python3
"""Independent differential test for HumanEval/22.

The oracle is imported from the trusted /reference/canonical.py mount.  The
candidate implementation is imported from the clean scratch copy, not from its
candidate-side __pycache__.
"""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


TRUSTED_CANONICAL = Path("/reference/canonical.py")
SCRATCH_SOLUTION = Path("/tmp/audit-work/22-filter-integers/src/solution.py")
SEED = 220022
GENERATED_CASES = 200


def load_entry(module_name: str, path: Path) -> Callable[[list[Any]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


class IntSubclass(int):
    pass


class PlainObject:
    pass


class ListSubclass(list[Any]):
    pass


PLAIN_OBJECT = PlainObject()


def describe(value: Any) -> dict[str, Any]:
    if isinstance(value, IntSubclass):
        return {"type": "IntSubclass", "value": int(value)}
    if type(value) is bool:
        return {"type": "bool", "value": value}
    if type(value) is int:
        return {"type": "int", "value": value}
    if type(value) is float:
        if math.isnan(value):
            rendered: Any = "nan"
        elif math.isinf(value):
            rendered = "inf" if value > 0 else "-inf"
        else:
            rendered = value
        return {"type": "float", "value": rendered}
    if isinstance(value, PlainObject):
        return {"type": "PlainObject"}
    if isinstance(value, ListSubclass):
        return {"type": "ListSubclass", "value": [describe(item) for item in value]}
    if isinstance(value, list):
        return {"type": "list", "value": [describe(item) for item in value]}
    if isinstance(value, tuple):
        return {"type": "tuple", "value": [describe(item) for item in value]}
    if isinstance(value, dict):
        return {
            "type": "dict",
            "value": [
                [describe(key), describe(item)]
                for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
            ],
        }
    if isinstance(value, set):
        return {
            "type": "set",
            "value": sorted((describe(item) for item in value), key=lambda item: repr(item)),
        }
    if isinstance(value, bytes):
        return {"type": "bytes", "value": value.hex()}
    if isinstance(value, complex):
        return {"type": "complex", "real": value.real, "imag": value.imag}
    return {"type": type(value).__name__, "value": value}


atoms: list[Any] = [
    -10**100,
    -2,
    -1,
    0,
    1,
    2,
    10**100,
    True,
    False,
    IntSubclass(-7),
    IntSubclass(0),
    IntSubclass(11),
    -0.0,
    2.0,
    float("inf"),
    float("-inf"),
    float("nan"),
    "",
    "abc",
    None,
    b"",
    b"\x00\xff",
    3 + 4j,
    (),
    (1, "x"),
    [],
    [1, "x"],
    ListSubclass([2, "y"]),
    {},
    {"k": 3},
    set(),
    {1, 2},
    PLAIN_OBJECT,
]

named_cases: list[tuple[str, list[Any]]] = [
    ("prompt_example_1", ["a", 3.14, 5]),
    ("prompt_example_2", [1, 2, 3, "abc", {}, []]),
    ("empty", []),
    ("predicate_true_exact_int", [0]),
    ("predicate_false_float", [0.0]),
    ("bool_subclass_boundary", [True, False]),
    ("user_int_subclass_boundary", [IntSubclass(-7), IntSubclass(0)]),
    ("large_and_negative", [-10**100, -1, 0, 10**100]),
    ("duplicates_and_order", [2, "skip", 2, False, -1, 2.0]),
    ("all_modeled_nonints", ["", 1.5, [], {}, None, PLAIN_OBJECT]),
    ("nested_values", [[1, 2], (3,), {"x": 4}, {5}, 6]),
]

rng = random.Random(SEED)
generated_cases: list[tuple[str, list[Any]]] = []
for case_index in range(GENERATED_CASES):
    case_length = rng.randrange(0, 25)
    values = [rng.choice(atoms) for _ in range(case_length)]
    generated_cases.append((f"generated_{case_index:03d}", values))

canonical = load_entry("trusted_canonical_22", TRUSTED_CANONICAL)
candidate = load_entry("scratch_candidate_22", SCRATCH_SOLUTION)

mismatches = 0
all_cases = named_cases + generated_cases
for name, values in all_cases:
    oracle_result = canonical(values)
    candidate_result = candidate(values)
    matched = (
        len(oracle_result) == len(candidate_result)
        and all(
            type(left) is type(right) and left == right
            for left, right in zip(oracle_result, candidate_result)
        )
    )
    if not matched:
        mismatches += 1
    print(
        json.dumps(
            {
                "case": name,
                "input": [describe(value) for value in values],
                "oracle": [describe(value) for value in oracle_result],
                "candidate": [describe(value) for value in candidate_result],
                "match": matched,
            },
            sort_keys=True,
            allow_nan=False,
        )
    )

print(
    json.dumps(
        {
            "summary": {
                "named_cases": len(named_cases),
                "generated_cases": len(generated_cases),
                "random_seed": SEED,
                "total_cases": len(all_cases),
                "mismatches": mismatches,
            }
        },
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)
