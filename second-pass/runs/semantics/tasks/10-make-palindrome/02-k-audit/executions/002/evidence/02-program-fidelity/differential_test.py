#!/usr/bin/env python3
"""Independent differential and contract checks for make_palindrome."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", ROOT / "reference/canonical.py")
generated = load_module("generated_solution", ROOT / "solution.py")


def brute_shortest(s: str) -> str:
    """Enumerate prefix-preserving palindrome completions by result length."""

    for added_length in range(len(s) + 1):
        candidate = s + s[:added_length][::-1]
        if candidate == candidate[::-1]:
            return candidate
    raise AssertionError("the full reversed prefix must always work")


documented = ["", "cat", "cata"]
branch_boundaries = [
    "x",       # first loop iteration succeeds, length one
    "aa",      # first loop iteration succeeds, already a palindrome
    "ab",      # first failure, second/last iteration succeeds
    "cata",    # first failure, internal suffix succeeds
    "cat",     # only the last single-character suffix succeeds
    "aaaa",    # all-equal palindrome
    "abac",    # nontrivial last-suffix completion
    "race",    # canonical common case
]
unicode_and_controls = [
    "\x00",
    "a\x00b",
    "éa",
    "🙂🙃",
    "🙂a🙂",
    "e\u0301x",
    "中ab",
    "\n\t",
]

exhaustive = [
    "".join(chars)
    for length in range(0, 9)
    for chars in itertools.product("abc", repeat=length)
]

rng = random.Random(0x10FACE)
random_alphabet = ["a", "b", "c", "é", "中", "🙂", "\x00"]
generated_random = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 61)))
    for _ in range(500)
]

cases: list[str] = []
seen: set[str] = set()
for value in (
    documented
    + branch_boundaries
    + unicode_and_controls
    + exhaustive
    + generated_random
):
    if value not in seen:
        seen.add(value)
        cases.append(value)

mismatches: list[dict[str, str]] = []
for value in cases:
    expected = brute_shortest(value)
    canonical_result = canonical.make_palindrome(value)
    generated_result = generated.make_palindrome(value)
    if not (
        canonical_result
        == generated_result
        == expected
        and generated_result.startswith(value)
        and generated_result == generated_result[::-1]
    ):
        mismatches.append(
            {
                "input": repr(value),
                "canonical": repr(canonical_result),
                "generated": repr(generated_result),
                "brute_shortest": repr(expected),
            }
        )

serialized_cases = json.dumps(
    cases, ensure_ascii=True, separators=(",", ":")
).encode()
print(f"documented_cases={len(documented)}")
print(f"branch_boundary_cases={len(branch_boundaries)}")
print(f"unicode_control_cases={len(unicode_and_controls)}")
print("exhaustive_alphabet='abc' lengths=0..8 generated=9841")
print("random_seed=0x10FACE random_generated=500 lengths=0..60")
print(f"unique_cases={len(cases)}")
print(f"inputs_json_sha256={hashlib.sha256(serialized_cases).hexdigest()}")
print("oracle=independent enumeration by increasing appended-prefix length")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2, ensure_ascii=True))
    raise SystemExit(1)
print("result=PASS")
