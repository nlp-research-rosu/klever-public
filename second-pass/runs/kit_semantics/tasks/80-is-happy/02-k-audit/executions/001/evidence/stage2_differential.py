#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval/80."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


def contract_oracle(text: str) -> bool:
    """Direct statement of: length >= 3 and each width-3 window is distinct."""
    return len(text) >= 3 and all(
        len({text[index], text[index + 1], text[index + 2]}) == 3
        for index in range(len(text) - 2)
    )


parser = argparse.ArgumentParser()
parser.add_argument("canonical", type=Path)
parser.add_argument("candidate", type=Path)
parser.add_argument("corpus_output", type=Path)
args = parser.parse_args()

canonical = load_entry(args.canonical, "audit_trusted_canonical")
candidate = load_entry(args.candidate, "audit_generated_solution")

documented = {
    "a": False,
    "aa": False,
    "abcd": True,
    "aabb": False,
    "adb": True,
    "xyy": False,
}
boundaries = [
    "",
    "a",
    "ab",
    "aa",
    "abc",
    "aab",
    "abb",
    "aba",
    "abcd",
    "abca",  # distance-three repetition is allowed
    "abac",
    "abcb",
    "aabc",
    "abbc",
    "abcc",
    "\x00\x01\x02",
    "\x00\x01\x00",
    "😀βγ😀",
    "😀β😀",
    "éｅ𝄞",
    "éｅé",
]

exhaustive = [
    "".join(chars)
    for length in range(0, 8)
    for chars in itertools.product("abc", repeat=length)
]

rng = random.Random(800080)
alphabet = ["a", "b", "c", "x", "é", "中", "😀", "\x00", "\U0010ffff"]
generated = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 81)))
    for _ in range(2500)
]
generated.extend(
    [
        "".join(chr(code) for code in range(1, 201)),
        "abc" * 4000,
        "".join(chr(0x10000 + offset) for offset in range(1000)),
    ]
)

all_cases: list[str] = []
seen: set[str] = set()
for text in list(documented) + boundaries + exhaustive + generated:
    if text not in seen:
        seen.add(text)
        all_cases.append(text)

args.corpus_output.write_text(
    json.dumps(
        {
            "seed": 800080,
            "random_alphabet_codepoints": [ord(char) for char in alphabet],
            "cases": all_cases,
        },
        ensure_ascii=True,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches: list[dict[str, object]] = []
for text in all_cases:
    expected_contract = contract_oracle(text)
    expected_canonical = canonical(text)
    actual = candidate(text)
    if text in documented and expected_canonical is not documented[text]:
        mismatches.append(
            {
                "kind": "documented/canonical",
                "input": repr(text),
                "documented": documented[text],
                "canonical": expected_canonical,
            }
        )
    if expected_canonical is not expected_contract:
        mismatches.append(
            {
                "kind": "contract/canonical",
                "input": repr(text),
                "contract": expected_contract,
                "canonical": expected_canonical,
            }
        )
    if actual is not expected_canonical:
        mismatches.append(
            {
                "kind": "candidate/canonical",
                "input": repr(text),
                "canonical": expected_canonical,
                "candidate": actual,
            }
        )

corpus_hash = hashlib.sha256(args.corpus_output.read_bytes()).hexdigest()
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_alphabet=abc exhaustive_lengths=0..7 count={len(exhaustive)}")
print(f"generated_seed=800080 generated_count={len(generated)}")
print(f"unique_total_cases={len(all_cases)}")
print(f"max_input_length={max(map(len, all_cases))}")
print(f"corpus_sha256={corpus_hash}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(json.dumps(mismatch, ensure_ascii=True, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
