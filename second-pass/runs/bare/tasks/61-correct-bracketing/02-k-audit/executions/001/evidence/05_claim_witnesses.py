#!/usr/bin/env python3
"""Ground witnesses for entry/loop preconditions and claimed results."""

from __future__ import annotations

import importlib.util
import json


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def bracket_spec(depth: int, suffix: str) -> bool:
    assert depth >= 0
    for char in suffix:
        if char == "(":
            depth += 1
        elif depth == 0:
            return False
        else:
            depth -= 1
    return depth == 0


canonical = load_entry("trusted_canonical_witness", "/reference/canonical.py")
generated = load_entry(
    "scratch_generated_witness", "/tmp/audit-work/candidate-src/solution.py"
)

entry_inputs = ["", "(()())", ")"]
loop_inputs = [
    {"N": 0, "S": "", "CURRENT": "", "ORIGINAL": ""},
    {"N": 2, "S": "))", "CURRENT": "(", "ORIGINAL": "(())"},
    {"N": 1, "S": "))", "CURRENT": "(", "ORIGINAL": "())"},
]

records = {"entry": [], "loop": []}
failure = False
for value in entry_inputs:
    claimed = bracket_spec(0, value)
    can = canonical(value)
    gen = generated(value)
    ok = claimed == can == gen
    failure |= not ok
    records["entry"].append(
        {
            "S": value,
            "precondition": "initial functions=.Map and env=.Map (realizable)",
            "claimed_bracketSpec_0_S": claimed,
            "canonical_python": can,
            "generated_python": gen,
            "match": ok,
        }
    )

for witness in loop_inputs:
    depth = witness["N"]
    suffix = witness["S"]
    prefixed_entry_input = "(" * depth + suffix
    claimed = bracket_spec(depth, suffix)
    can = canonical(prefixed_entry_input)
    gen = generated(prefixed_entry_input)
    ok = claimed == can == gen
    failure |= not ok
    records["loop"].append(
        {
            **witness,
            "precondition": f"N={depth} >= 0; exact three-entry env is realizable",
            "equivalent_entry_input": prefixed_entry_input,
            "claimed_bracketSpec_N_S": claimed,
            "canonical_python": can,
            "generated_python": gen,
            "match": ok,
        }
    )

print(json.dumps(records, indent=2))
raise SystemExit(1 if failure else 0)
