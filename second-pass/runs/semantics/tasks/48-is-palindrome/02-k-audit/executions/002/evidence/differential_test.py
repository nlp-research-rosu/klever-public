#!/usr/bin/env python3
"""Independent differential test for HumanEval/48 over Python string inputs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import pathlib
import random
import sys
from types import ModuleType


def load_module(name: str, path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_two_pointer(text: str) -> bool:
    left = 0
    right = len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True


parser = argparse.ArgumentParser()
parser.add_argument("--canonical", type=pathlib.Path, required=True)
parser.add_argument("--generated", type=pathlib.Path, required=True)
parser.add_argument("--inputs-out", type=pathlib.Path, required=True)
args = parser.parse_args()

canonical = load_module("trusted_canonical", args.canonical).is_palindrome
generated = load_module("candidate_generated", args.generated).is_palindrome

cases: list[dict[str, str]] = []


def add(source: str, label: str, text: str) -> None:
    cases.append({"source": source, "label": label, "text": text})


prompt_cases = {
    "prompt-empty-true": ("", True),
    "prompt-odd-true": ("aba", True),
    "prompt-repeated-true": ("aaaaa", True),
    "prompt-first-mismatch-false": ("zbcd", False),
}
for label, (text, _expected) in prompt_cases.items():
    add("prompt", label, text)

boundary_cases = {
    "length-one": "x",
    "length-two-equal": "xx",
    "length-two-mismatch": "xy",
    "even-palindrome": "abccba",
    "even-center-mismatch": "abdcba",
    "odd-palindrome": "abcba",
    "odd-inner-mismatch": "abcca",
    "outer-mismatch": "xbcba",
    "embedded-nul-palindrome": "a\x00a",
    "combining-sequence-palindrome": "e\u0301\u0301e",
    "emoji-palindrome": "😀中😀",
    "newline-mismatch": "a\nb",
}
for label, text in boundary_cases.items():
    add("boundary", label, text)

exhaustive_alphabet = ("a", "b", "☃")
for length in range(0, 9):
    for index, chars in enumerate(itertools.product(exhaustive_alphabet, repeat=length)):
        add("exhaustive", f"alphabet3-length{length}-index{index}", "".join(chars))

random_seed = 480048
random_generator = random.Random(random_seed)
random_alphabet = ("a", "b", "0", "\x00", "é", "e", "\u0301", "😀", "中", "\n")
for index in range(2000):
    length = random_generator.randrange(0, 65)
    text = "".join(random_generator.choice(random_alphabet) for _ in range(length))
    add("generated-random", f"seed{random_seed}-index{index}", text)

encoded_inputs = json.dumps(
    {
        "schema": 1,
        "random_seed": random_seed,
        "exhaustive_alphabet": exhaustive_alphabet,
        "exhaustive_lengths": [0, 8],
        "random_alphabet": random_alphabet,
        "random_count": 2000,
        "cases": cases,
    },
    ensure_ascii=False,
    indent=2,
    sort_keys=True,
).encode("utf-8")
args.inputs_out.write_bytes(encoded_inputs)

mismatches: list[dict[str, object]] = []
for case in cases:
    text = case["text"]
    canonical_result = canonical(text)
    generated_result = generated(text)
    independent_result = independent_two_pointer(text)
    if (
        type(canonical_result) is not bool
        or type(generated_result) is not bool
        or canonical_result != generated_result
        or canonical_result != independent_result
    ):
        mismatches.append(
            {
                **case,
                "canonical": canonical_result,
                "generated": generated_result,
                "independent": independent_result,
                "canonical_type": type(canonical_result).__name__,
                "generated_type": type(generated_result).__name__,
            }
        )

for label, (text, expected) in prompt_cases.items():
    actual = generated(text)
    if actual is not expected:
        mismatches.append(
            {
                "source": "prompt-expected",
                "label": label,
                "text": text,
                "expected": expected,
                "generated": actual,
            }
        )

source_counts: dict[str, int] = {}
for case in cases:
    source_counts[case["source"]] = source_counts.get(case["source"], 0) + 1

print(f"canonical={args.canonical}")
print(f"generated={args.generated}")
print(f"input_file={args.inputs_out}")
print(f"input_file_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
print(f"source_counts={json.dumps(source_counts, sort_keys=True)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], ensure_ascii=False, indent=2, default=repr))
    sys.exit(1)
print("RESULT=ZERO_MISMATCHES")
