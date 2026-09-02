#!/usr/bin/env python3
"""Independent deterministic differential tests for HumanEval/38."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
prompt = load_module("trusted_prompt", Path("/reference/prompt.py"))
generated = load_module("generated_solution", Path("/candidate/solution.py"))

# The first eight inputs hit the empty case, both short-tail cases, entry into
# the loop at length 3, and both sides of each subsequent remainder boundary.
boundary_inputs = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "abcdefgh",
    "Hello, world!",
    "\"'\\\n\t\x00",
    "éα中🙂𝄞",
    "e\u0301🙂中A",
]

alphabet = [
    "a",
    "Z",
    "0",
    " ",
    "\n",
    "\t",
    "\x00",
    "\"",
    "\\",
    "é",
    "\u0301",
    "α",
    "中",
    "🙂",
    "𝄞",
]
seed = 0x38DEC0DE
rng = random.Random(seed)
generated_inputs = [
    "".join(rng.choice(alphabet) for _ in range(length))
    for length in range(65)
    for _ in range(64)
]
inputs = boundary_inputs + generated_inputs

mismatches: list[dict[str, str]] = []
inverse_failures: list[dict[str, str]] = []
corpus_hash = hashlib.sha256()

for value in inputs:
    corpus_hash.update(json.dumps(value, ensure_ascii=True).encode("ascii") + b"\n")
    expected = canonical.decode_cyclic(value)
    actual = generated.decode_cyclic(value)
    if actual != expected:
        mismatches.append(
            {"input": repr(value), "canonical": repr(expected), "generated": repr(actual)}
        )

    encoded = prompt.encode_cyclic(value)
    decoded = generated.decode_cyclic(encoded)
    if decoded != value:
        inverse_failures.append(
            {"source": repr(value), "encoded": repr(encoded), "decoded": repr(decoded)}
        )

print("ORACLE: /reference/canonical.py decode_cyclic")
print("GENERATED: /candidate/solution.py decode_cyclic")
print("INVERSE ENCODER: /reference/prompt.py encode_cyclic")
print("EXPLICIT_PROMPT_EXAMPLES: none")
print(f"BOUNDARY_INPUTS: {len(boundary_inputs)}")
print(f"GENERATED_INPUTS: {len(generated_inputs)}")
print(f"TOTAL_INPUTS: {len(inputs)}")
print(f"RANDOM_SEED: {seed}")
print(f"ALPHABET_JSON: {json.dumps(alphabet, ensure_ascii=True)}")
print(f"CORPUS_SHA256: {corpus_hash.hexdigest()}")
print(f"DIFFERENTIAL_MISMATCHES: {len(mismatches)}")
print(f"INVERSE_FAILURES: {len(inverse_failures)}")

if mismatches:
    print("FIRST_DIFFERENTIAL_MISMATCH:")
    print(json.dumps(mismatches[0], ensure_ascii=True, sort_keys=True))
if inverse_failures:
    print("FIRST_INVERSE_FAILURE:")
    print(json.dumps(inverse_failures[0], ensure_ascii=True, sort_keys=True))

sys.exit(1 if mismatches or inverse_failures else 0)
