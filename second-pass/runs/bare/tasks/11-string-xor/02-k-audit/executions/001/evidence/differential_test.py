#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test.

The exhaustive scope is all pairs of binary strings of lengths 0..6.
The generated scope is 512 deterministic pairs of lengths 0..96.
Explicit cases cover the prompt example, empty inputs, unequal lengths, both
head-bit branches, and a valid input just beyond CPython's recursion ceiling.
Every generated input is recorded in differential-inputs.jsonl.
"""

from __future__ import annotations

import importlib.util
import itertools
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Callable


EVIDENCE = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/11-string-xor-audit/source/solution.py")
INPUTS_PATH = EVIDENCE / "differential-inputs.jsonl"


def load_entry(path: Path, module_name: str) -> Callable[[str, str], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "scratch_candidate")


def binaries(length: int):
    if length == 0:
        yield ""
        return
    for chars in itertools.product("01", repeat=length):
        yield "".join(chars)


cases: list[tuple[str, str, str]] = [
    ("prompt-example", "010", "110"),
    ("both-empty", "", ""),
    ("left-empty", "", "101"),
    ("right-empty", "101", ""),
    ("equal-head", "00", "01"),
    ("unequal-head", "10", "00"),
    ("left-shorter", "01", "110101"),
    ("right-shorter", "110101", "01"),
]

for left_len in range(7):
    lefts = list(binaries(left_len))
    for right_len in range(7):
        rights = list(binaries(right_len))
        for left in lefts:
            for right in rights:
                cases.append(("exhaustive-0..6", left, right))

rng = random.Random(0x11_58_4F_52)
for _ in range(512):
    left_len = rng.randrange(97)
    right_len = rng.randrange(97)
    left = "".join(rng.choice("01") for _ in range(left_len))
    right = "".join(rng.choice("01") for _ in range(right_len))
    cases.append(("generated-512-seed-0x11584f52", left, right))

long_len = sys.getrecursionlimit() + 100
cases.append(
    (
        "recursion-boundary-valid-domain",
        ("01" * ((long_len + 1) // 2))[:long_len],
        ("10" * ((long_len + 1) // 2))[:long_len],
    )
)


def observe(fn: Callable[[str, str], str], left: str, right: str):
    try:
        return {"kind": "return", "value": fn(left, right)}
    except BaseException as err:  # capture the observable divergence
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def bounded(observation):
    if observation.get("kind") != "return":
        return observation
    value = observation["value"]
    return {
        "kind": "return",
        "length": len(value),
        "sha256": hashlib.sha256(value.encode()).hexdigest(),
        "prefix": value[:32],
    }


mismatches = []
with INPUTS_PATH.open("w", encoding="utf-8") as inputs_file:
    for index, (scope, left, right) in enumerate(cases):
        record = {"index": index, "scope": scope, "a": left, "b": right}
        inputs_file.write(json.dumps(record, sort_keys=True) + "\n")
        expected = observe(canonical, left, right)
        actual = observe(candidate, left, right)
        if expected != actual:
            mismatch = {
                "index": index,
                "scope": scope,
                "a_length": len(left),
                "b_length": len(right),
                "canonical": bounded(expected),
                "candidate": bounded(actual),
            }
            mismatches.append(mismatch)
            print("MISMATCH " + json.dumps(mismatch, sort_keys=True))

scope_counts: dict[str, int] = {}
for scope, _, _ in cases:
    scope_counts[scope] = scope_counts.get(scope, 0) + 1

print(
    json.dumps(
        {
            "canonical_path": str(CANONICAL_PATH),
            "candidate_path": str(CANDIDATE_PATH),
            "case_count": len(cases),
            "scope_counts": scope_counts,
            "mismatch_count": len(mismatches),
            "inputs_artifact": str(INPUTS_PATH),
        },
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)
