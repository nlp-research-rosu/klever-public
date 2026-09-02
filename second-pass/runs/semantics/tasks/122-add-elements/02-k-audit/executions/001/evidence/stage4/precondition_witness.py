#!/usr/bin/env python3
"""Ground witnesses for the K entry and loop preconditions and postcondition."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int], int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add_elements


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_witness")
submitted = load_entry(Path("/tmp/audit-work/src/solution.py"), "submitted_witness")


def qualifying_sum_acc(acc: int, values: list[int]) -> int:
    for value in values:
        if abs(value) < 100:
            acc += value
    return acc


def entry_record(head: int, prefix: list[int], suffix: list[int]) -> dict[str, object]:
    selected_prefix = [head, *prefix]
    full_array = [*selected_prefix, *suffix]
    k = len(selected_prefix)
    precondition = (
        isinstance(head, int)
        and all(isinstance(value, int) for value in prefix)
        and all(isinstance(value, int) for value in suffix)
        and len(selected_prefix) + len(suffix) <= 100
    )
    return {
        "head": head,
        "prefix": prefix,
        "suffix": suffix,
        "array": full_array,
        "k": k,
        "entry_precondition": precondition,
        "claimed_result": qualifying_sum_acc(0, selected_prefix),
        "submitted_python": submitted(full_array, k),
        "trusted_canonical": canonical(full_array, k),
    }


records = [
    entry_record(21, [3], [4000]),
    entry_record(-99, [], []),
]
loop_witness = {
    "globals": {},
    "abs_not_shadowed": "abs" not in {},
    "arr": [-99],
    "k": 1,
    "acc": 0,
    "old_element": 1234,
    "v": -99,
    "vs": [],
    "loop_precondition": isinstance(-99, int) and all(
        isinstance(value, int) for value in []
    ),
    "claimed_final_total": qualifying_sum_acc(0, [-99]),
}

print("ENTRY_WITNESSES_JSON:")
print(json.dumps(records, sort_keys=True))
print("LOOP_WITNESS_JSON:")
print(json.dumps(loop_witness, sort_keys=True))

assert all(record["entry_precondition"] for record in records)
assert loop_witness["abs_not_shadowed"] and loop_witness["loop_precondition"]
assert records[0]["claimed_result"] == records[0]["submitted_python"] == 24
assert records[0]["trusted_canonical"] == 24
assert records[1]["claimed_result"] == records[1]["submitted_python"] == -99
assert records[1]["trusted_canonical"] == 0
