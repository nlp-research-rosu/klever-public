#!/usr/bin/env python3
"""Independent differential checks for HumanEval 14."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.all_prefixes


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/tmp/audit-work/rebuild/solution.py"), "candidate_solution")

fixed = [
    "",
    "a",
    "ab",
    "abc",
    "aaaa",
    " ",
    "\n",
    "\x00",
    "\"\\",
    "é",
    "e\u0301",
    "🙂",
    "🙂a",
    "a🙂b",
    "漢字",
    "a" * 1000,
]

rng = random.Random(140014)
alphabet = ["a", "b", "Z", "0", " ", "\n", "é", "\u0301", "🙂", "漢"]
generated_inputs = [
    "".join(rng.choice(alphabet) for _ in range(length))
    for length in [0, 1, 2, 3, 4, 7, 16, 32]
    for _ in range(8)
]
inputs = fixed + generated_inputs

mismatches = []
serialized_inputs = []
for index, string in enumerate(inputs):
    canonical_result = canonical(string)
    generated_result = generated(string)
    independent_result = [string[:i] for i in range(1, len(string) + 1)]
    serialized_inputs.append(string)
    if canonical_result != generated_result or canonical_result != independent_result:
        mismatches.append(
            {
                "index": index,
                "input": string,
                "canonical": canonical_result,
                "generated": generated_result,
                "independent": independent_result,
            }
        )

encoded_inputs = json.dumps(
    serialized_inputs, ensure_ascii=True, separators=(",", ":")
).encode()
print("contract=all nonempty prefixes, shortest to longest")
print(f"case_count={len(inputs)}")
print(f"inputs_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
print("inputs=" + encoded_inputs.decode())
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("mismatches=" + json.dumps(mismatches, ensure_ascii=True, sort_keys=True))
    raise SystemExit(1)
print("RESULT=PASS")
