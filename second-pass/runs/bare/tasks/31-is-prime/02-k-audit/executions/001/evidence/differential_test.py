#!/usr/bin/env python3
"""Independent differential test for HumanEval problem 31.

The trusted reference and submitted implementation are loaded from the clean
scratch copies.  Bytecode writing is disabled by the invoking command.
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/candidate-src/solution.py")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def outcome(function, *args):
    try:
        return {"kind": "return", "value": function(*args)}
    except Exception as err:  # The no-argument case deliberately reaches here.
        return {"kind": "exception", "type": type(err).__name__}


canonical = load_entry("trusted_canonical", TRUSTED)
generated = load_entry("submitted_generated", GENERATED)

documented = [6, 101, 11, 13441, 61, 4, 1]
boundaries = [
    -100,
    -2,
    -1,
    0,
    1,
    2,
    3,
    4,
    5,
    7,
    8,
    9,
    10,
    15,
    16,
    17,
    24,
    25,
    26,
    48,
    49,
    50,
    120,
    121,
    122,
]
recursion_boundaries = [
    1_000_003,  # prime; trial divisors pass Python's default recursion depth
    1_022_117,  # 1009 * 1013; first divisor also lies beyond that depth
]
exhaustive_small = list(range(-250, 2001))
rng = random.Random(310031)
generated_sample = [rng.randint(-5000, 20000) for _ in range(512)]
inputs = sorted(
    set(
        documented
        + boundaries
        + recursion_boundaries
        + exhaustive_small
        + generated_sample
    )
)

mismatches = []
for value in inputs:
    left = outcome(canonical, value)
    right = outcome(generated, value)
    if left != right:
        mismatches.append({"input": value, "canonical": left, "generated": right})

# "Empty" has no in-domain scalar representation, so also check the empty
# argument list as an explicit arity-boundary case.
empty_call = {
    "args": [],
    "canonical": outcome(canonical),
    "generated": outcome(generated),
}
if empty_call["canonical"] != empty_call["generated"]:
    mismatches.append({"empty_call": empty_call})

print(
    json.dumps(
        {
            "oracle": str(TRUSTED),
            "implementation": str(GENERATED),
            "documented": documented,
            "boundaries": boundaries,
            "recursion_boundaries": recursion_boundaries,
            "exhaustive_small": {"start": -250, "stop_inclusive": 2000},
            "random": {
                "seed": 310031,
                "count_before_deduplication": 512,
                "range_inclusive": [-5000, 20000],
            },
            "all_integer_inputs": inputs,
            "integer_input_count": len(inputs),
            "empty_argument_case": empty_call,
            "mismatches": mismatches,
            "mismatch_count": len(mismatches),
        },
        sort_keys=True,
    )
)

raise SystemExit(1 if mismatches else 0)
