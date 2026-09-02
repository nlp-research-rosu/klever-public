#!/usr/bin/env python3
"""Independent differential and contract checks for make_palindrome."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
import sys
from pathlib import Path


sys.dont_write_bytecode = True


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical_module = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate_module = load_module(
    "generated_solution", Path("/tmp/audit-work/candidate/solution.py")
)


def shortest_palindrome_by_definition(value: str) -> str:
    for split in range(len(value) + 1):
        suffix = value[split:]
        if suffix == suffix[::-1]:
            return value + value[:split][::-1]
    raise AssertionError("the one-character/empty suffix must be palindromic")


def outcome(function, value: str) -> tuple[str, object]:
    try:
        return ("return", function(value))
    except BaseException as error:  # Deliberately compare observable exceptions.
        return ("raise", (type(error).__name__, str(error)))


documented = ["", "cat", "cata"]
boundaries = [
    "a",
    "aa",
    "ab",
    "aba",
    "abb",
    "abba",
    "abc",
    "abca",
    "aaaa",
    "aab",
    "aabb",
    "abac",
    "race",
    "\x00",
    "\n",
    "😀",
    "😀a",
    "e\u0301",
    "λ漢🙂",
]
exhaustive = [
    "".join(chars)
    for size in range(8)
    for chars in itertools.product("abc", repeat=size)
]
rng = random.Random(10010)
generated = [
    "".join(rng.choice("abcxyz012!?") for _ in range(rng.randrange(65)))
    for _ in range(500)
]
normal_cases = list(dict.fromkeys(documented + boundaries + exhaustive + generated))

mismatches: list[tuple[str, tuple[str, object], tuple[str, object]]] = []
property_failures: list[tuple[str, object, str]] = []
for value in normal_cases:
    expected = outcome(canonical_module.make_palindrome, value)
    actual = outcome(candidate_module.make_palindrome, value)
    if actual != expected:
        mismatches.append((value, expected, actual))
    if expected[0] == "return":
        definition_result = shortest_palindrome_by_definition(value)
        if expected[1] != definition_result:
            property_failures.append((value, expected[1], definition_result))

print(f"documented_cases={len(documented)}")
print(f"named_boundary_cases={len(boundaries)}")
print("exhaustive_scope=alphabet:'abc', lengths:0..7")
print(f"exhaustive_cases={len(exhaustive)}")
print("generated_scope=seed:10010, alphabet:'abcxyz012!?', lengths:0..64")
print(f"generated_cases={len(generated)}")
print(f"distinct_normal_cases={len(normal_cases)}")
print(f"normal_mismatches={len(mismatches)}")
print(f"canonical_contract_failures={len(property_failures)}")
for value in documented + boundaries:
    print(
        "case="
        f"{value!r} canonical={outcome(canonical_module.make_palindrome, value)!r} "
        f"candidate={outcome(candidate_module.make_palindrome, value)!r}"
    )

# A valid unrestricted Python str whose unique code points force one recursive
# call per character until the final one-character palindrome.
long_unique = "".join(chr(0x1000 + index) for index in range(1100))
long_expected = outcome(canonical_module.make_palindrome, long_unique)
long_actual = outcome(candidate_module.make_palindrome, long_unique)
print("long_boundary_scope=1100 distinct Unicode code points U+1000..U+144B")
print(f"python_recursion_limit={sys.getrecursionlimit()}")
if long_expected[0] == "return":
    encoded = str(long_expected[1]).encode("utf-8")
    print(f"long_canonical=return length:{len(long_expected[1])}")
    print(f"long_canonical_utf8_sha256={hashlib.sha256(encoded).hexdigest()}")
else:
    print(f"long_canonical={long_expected!r}")
print(f"long_candidate={long_actual!r}")

all_normal_ok = not mismatches and not property_failures
long_matches = long_actual == long_expected
print(f"NORMAL_DIFFERENTIAL={'PASS' if all_normal_ok else 'FAIL'}")
print(f"LONG_BOUNDARY_DIFFERENTIAL={'PASS' if long_matches else 'FAIL'}")
raise SystemExit(0 if all_normal_ok and long_matches else 1)
