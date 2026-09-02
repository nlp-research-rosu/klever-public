#!/usr/bin/env python3
"""Ground witnesses for every formal precondition and entry result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_up_to


def no_divisor(candidate: int, divisor: int, high: int) -> bool:
    if divisor >= high:
        return True
    if candidate % divisor == 0:
        return False
    return no_divisor(candidate, divisor + 1, high)


def append_if_prime(values: list[int], candidate: int, flag: bool) -> list[int]:
    return values if not flag else values + [candidate]


def primes_acc(values: list[int], candidate: int, bound: int) -> list[int]:
    while candidate < bound:
        values = append_if_prime(
            values, candidate, no_divisor(candidate, 2, candidate)
        )
        candidate += 1
    return values


canonical = load_entry("trusted_ground", Path("/reference/canonical.py"))
generated = load_entry("generated_ground", Path("/candidate/solution.py"))

witnesses = {
    "inner_loop": {
        "C": 5,
        "D": 2,
        "B": True,
        "N": 20,
        "VS": [],
        "precondition": 2 <= 2 <= 5,
    },
    "outer_loop": {
        "I": 2,
        "N": 20,
        "VS": [],
        "precondition": 2 <= 2 <= 20,
    },
    "entry_main": {"N": 20, "precondition": 20 >= 2},
    "entry_boundary": {
        "N": 0,
        "precondition": 0 <= 0 < 2,
    },
}
print("satisfying_witnesses=" + json.dumps(witnesses, sort_keys=True))
if not all(item["precondition"] for item in witnesses.values()):
    raise AssertionError("one precondition witness is not satisfying")

for n in [20, 0]:
    claimed = primes_acc([], 2, n) if n >= 2 else []
    trusted = canonical(n)
    actual = generated(n)
    print(
        f"N={n} claimed_primesAcc={claimed} "
        f"trusted_canonical={trusted} generated={actual}"
    )
    if claimed != trusted or claimed != actual:
        raise AssertionError(f"ground result mismatch at N={n}")

inner_final_divisor = witnesses["inner_loop"]["C"]
inner_final_flag = witnesses["inner_loop"]["B"] and no_divisor(
    witnesses["inner_loop"]["C"],
    witnesses["inner_loop"]["D"],
    witnesses["inner_loop"]["C"],
)
print(
    "inner_loop_claimed_updates="
    + json.dumps(
        {
            "divisor": inner_final_divisor,
            "is_prime": inner_final_flag,
        },
        sort_keys=True,
    )
)
print("RESULT=PASS")
