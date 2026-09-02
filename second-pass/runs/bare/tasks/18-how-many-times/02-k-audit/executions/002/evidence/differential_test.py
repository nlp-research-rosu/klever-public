#!/usr/bin/env python3
import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.how_many_times


canonical = load_function("trusted_canonical", "/reference/canonical.py")
generated = load_function("candidate_solution", "/tmp/audit-work/src/solution.py")

cases = [
    ("", "a"),
    ("aaa", "a"),
    ("aaaa", "aa"),
    ("", ""),
    ("a", ""),
    ("abc", ""),
    ("a", "aa"),
    ("ab", "abc"),
    ("a", "a"),
    ("a", "b"),
    ("ab", "ab"),
    ("ab", "ac"),
    ("aaaaa", "aa"),
    ("abababa", "aba"),
    ("abababa", "bab"),
    ("abc", "z"),
    ("abcabc", "abc"),
    ("banana", "ana"),
    ("ééé", "éé"),
    ("🙂🙂🙂", "🙂🙂"),
    ("a🙂a🙂a", "a🙂a"),
    ("\x00a\x00a", "\x00a"),
    ("a" * 900, "b"),
    ("a" * 1000, "b"),
    ("a" * 1100, "b"),
    ("a" * 1100, "a"),
    ("ab" * 600, "ab"),
]

# Exhaust every pair over a small alphabet through all important length
# relations, then add reproducible broader ASCII/Unicode samples.
alphabet = "ab"
small_strings = [
    "".join(chars)
    for length in range(0, 7)
    for chars in itertools.product(alphabet, repeat=length)
]
small_substrings = [
    "".join(chars)
    for length in range(0, 5)
    for chars in itertools.product(alphabet, repeat=length)
]
cases.extend(itertools.product(small_strings, small_substrings))

rng = random.Random(180018)
wide_alphabet = "abcXYZ01 é🙂\x00"
for _ in range(2000):
    string = "".join(rng.choice(wide_alphabet) for _ in range(rng.randrange(0, 25)))
    substring = "".join(rng.choice(wide_alphabet) for _ in range(rng.randrange(0, 9)))
    cases.append((string, substring))

seen = set()
mismatches = []
checked = 0


def outcome(function, string, substring):
    try:
        return ("value", function(string, substring))
    except Exception as error:
        return ("exception", type(error).__name__, str(error))


for string, substring in cases:
    if (string, substring) in seen:
        continue
    seen.add((string, substring))
    expected = outcome(canonical, string, substring)
    actual = outcome(generated, string, substring)
    checked += 1
    if actual != expected:
        mismatches.append((string, substring, expected, actual))

print(f"documented_examples=3")
print(f"hand_boundary_cases=22")
print(f"recursion_stress_cases=5 max_string_len=1200")
print(f"python_recursion_limit={sys.getrecursionlimit()}")
print(f"exhaustive_binary_string_max_len=6")
print(f"exhaustive_binary_substring_max_len=4")
print(f"seed=180018 random_generated=2000")
print(f"unique_cases_checked={checked}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    string, substring, expected, actual = mismatch
    print(
        "MISMATCH",
        f"string_len={len(string)}",
        f"substring_len={len(substring)}",
        f"string_prefix={string[:24]!r}",
        f"substring={substring!r}",
        f"canonical={expected!r}",
        f"candidate={actual!r}",
    )
sys.exit(1 if mismatches else 0)
