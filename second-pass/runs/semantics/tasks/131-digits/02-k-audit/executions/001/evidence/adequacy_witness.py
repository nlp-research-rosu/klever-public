#!/usr/bin/env python3
"""Concrete satisfying witnesses for both submitted reachability claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/audit-131-digits")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def odd_digit_product(n: int, accumulator: int) -> int:
    """Direct evaluator for verification.k's defining recurrence."""
    assert n >= 0
    while n > 0:
        digit = n % 10
        if n % 2 == 1:
            accumulator = digit if accumulator == 0 else accumulator * digit
        n = (n - digit) // 10
    return accumulator


canonical = load_module("witness_canonical", WORK / "trusted" / "canonical.py")
candidate = load_module("witness_candidate", WORK / "candidate" / "solution.py")

entry_n = 235
entry = {
    "claim": "digits-correct",
    "precondition": f"N={entry_n} > 0",
    "formal_post_term": f"oddDigitProduct({entry_n}, 0)",
    "formal_post_value": odd_digit_product(entry_n, 0),
    "canonical_value": canonical.digits(entry_n),
    "candidate_value": candidate.digits(entry_n),
}

loop_n = 235
loop_a = 0
loop = {
    "claim": "digits-loop",
    "precondition": f"N={loop_n} >= 0 and A={loop_a} >= 0",
    "realizable_state": (
        "after digits(235) binds n=235 and executes product=0, immediately "
        "before the submitted while loop"
    ),
    "formal_post_bindings": {
        "n": 0,
        "product": odd_digit_product(loop_n, loop_a),
    },
}

print(json.dumps(entry, indent=2, sort_keys=True))
print(json.dumps(loop, indent=2, sort_keys=True))

assert entry["formal_post_value"] == 15
assert entry["formal_post_value"] == entry["canonical_value"]
assert entry["formal_post_value"] == entry["candidate_value"]
assert loop["formal_post_bindings"] == {"n": 0, "product": 15}
