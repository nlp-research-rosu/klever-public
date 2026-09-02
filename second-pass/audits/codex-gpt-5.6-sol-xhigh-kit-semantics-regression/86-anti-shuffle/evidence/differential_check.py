#!/usr/bin/env python3
"""Independent differential and contract check for HumanEval 86."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/02-differential-inputs.json")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def insertion_sort_word(word: str) -> str:
    ordered: list[str] = []
    for char in word:
        index = len(ordered)
        while index > 0 and ord(char) < ord(ordered[index - 1]):
            index -= 1
        ordered.insert(index, char)
    return "".join(ordered)


def contract_oracle(text: str) -> str:
    return " ".join(insertion_sort_word(word) for word in text.split(" "))


documented = [
    "Hi",
    "hello",
    "Hello World!!!",
]

boundaries = [
    "",
    " ",
    "  ",
    "   ",
    "a",
    "ab",
    "ba",
    "a ",
    " a",
    " a ",
    "a  b",
    "  ba  dc  ",
    "!~",
    "~!",
    "\x00 a",
    "\t a\n",
    "éA",
    "😀 a",
]

alphabet = " !0Aa~"
exhaustive = [
    "".join(chars)
    for length in range(6)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(860086)
random_alphabet = " !09AZaz~\t\néΩ😀"
generated = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 21)))
    for _ in range(2000)
]

inputs = list(dict.fromkeys(documented + boundaries + exhaustive + generated))
INPUTS_PATH.write_text(
    json.dumps(inputs, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "candidate_solution")

canonical_mismatches = []
contract_mismatches = []
for text in inputs:
    expected = canonical(text)
    actual = candidate(text)
    contract = contract_oracle(text)
    if actual != expected:
        canonical_mismatches.append((text, expected, actual))
    if actual != contract or expected != contract:
        contract_mismatches.append((text, expected, actual, contract))

encoded_inputs = json.dumps(
    inputs, ensure_ascii=False, separators=(",", ":")
).encode("utf-8")
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_alphabet={alphabet!r}")
print("exhaustive_lengths=0..5")
print(f"exhaustive_generated={len(exhaustive)}")
print("random_seed=860086")
print("random_lengths=0..20")
print(f"random_generated={len(generated)}")
print(f"unique_total={len(inputs)}")
print(f"inputs_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
print(f"canonical_mismatches={len(canonical_mismatches)}")
print(f"contract_mismatches={len(contract_mismatches)}")
for text in documented + boundaries:
    print(
        "case "
        + json.dumps(
            {
                "input": text,
                "canonical": canonical(text),
                "candidate": candidate(text),
                "contract": contract_oracle(text),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
if canonical_mismatches or contract_mismatches:
    print(f"first_canonical_mismatches={canonical_mismatches[:10]!r}")
    print(f"first_contract_mismatches={contract_mismatches[:10]!r}")
    raise SystemExit(1)
