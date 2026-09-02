#!/usr/bin/env python3
"""Independent differential test for HumanEval 48 over the intended str domain."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import pathlib
import random
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "is_palindrome")
    return entry


parser = argparse.ArgumentParser()
parser.add_argument("--canonical", type=pathlib.Path, required=True)
parser.add_argument("--solution", type=pathlib.Path, required=True)
parser.add_argument("--inputs-out", type=pathlib.Path, required=True)
args = parser.parse_args()

canonical = load_entry(args.canonical, "audit_trusted_canonical")
solution = load_entry(args.solution, "audit_candidate_solution")

documented = ["", "aba", "aaaaa", "zbcd"]
curated = [
    # Length and equality boundaries.
    "a",
    "aa",
    "ab",
    "aba",
    "abb",
    "abba",
    "abca",
    "abcba",
    "abcdef",
    # Mismatch at the first/last pair, an interior pair, and the center boundary.
    "xbcba",
    "axcya",
    "abxda",
    # Characters relevant to Python str rather than byte reversal.
    "été",
    "éaé",
    "🙂a🙂",
    "🙂🙃",
    "a\u0301a",
    "a\u0301\u0301a",
    "\x00",
    "\x00a\x00",
    "\n\t\n",
    "\"\\\"",
    # Larger boundary cases.
    "a" * 1024,
    "a" * 511 + "b" + "a" * 511,
    "a" * 511 + "bc" + "a" * 511,
]

alphabet = ("a", "b", "0", "é", "🙂", "\u0301")
exhaustive = [
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(480048)
random_alphabet = alphabet + (" ", "\n", "\x00", "ß", "中", "🙃")
generated = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 65)))
    for _ in range(1000)
]

# Deduplicate while retaining the order and provenance of first occurrence.
cases: list[tuple[str, str]] = []
seen: set[str] = set()
for category, values in [
    ("documented", documented),
    ("curated-boundary", curated),
    ("exhaustive-alphabet-length-0-through-5", exhaustive),
    ("seeded-random-480048", generated),
]:
    for value in values:
        if value not in seen:
            seen.add(value)
            cases.append((category, value))

mismatches: list[dict[str, object]] = []
input_digest = hashlib.sha256()
true_count = 0
false_count = 0

with args.inputs_out.open("w", encoding="utf-8") as inputs_file:
    for index, (category, value) in enumerate(cases):
        expected = canonical(value)
        actual = solution(value)
        if expected:
            true_count += 1
        else:
            false_count += 1
        record = {
            "index": index,
            "category": category,
            "input": value,
            "canonical": expected,
            "solution": actual,
        }
        serialized = json.dumps(record, ensure_ascii=True, sort_keys=True)
        inputs_file.write(serialized + "\n")
        input_digest.update((serialized + "\n").encode())
        if (
            actual != expected
            or not isinstance(actual, bool)
            or not isinstance(expected, bool)
        ):
            mismatches.append(record)

print("contract_domain=all Python str values")
print(f"canonical={args.canonical}")
print(f"solution={args.solution}")
print(f"documented_count={len(documented)}")
print(f"curated_count={len(curated)}")
print(f"exhaustive_alphabet={alphabet!r}")
print("exhaustive_lengths=0..5")
print("random_seed=480048")
print(f"seeded_random_attempts={len(generated)}")
print(f"unique_total={len(cases)}")
print(f"true_count={true_count}")
print(f"false_count={false_count}")
print(f"inputs_sha256={input_digest.hexdigest()}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH " + json.dumps(mismatch, ensure_ascii=True, sort_keys=True))

raise SystemExit(1 if mismatches else 0)
