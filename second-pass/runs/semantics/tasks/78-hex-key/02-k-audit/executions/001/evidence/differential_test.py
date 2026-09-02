#!/usr/bin/env python3
"""Independent finite differential test for HumanEval 78 hex_key."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/78-hex-key/solution.py")
INPUT_LOG = Path("/audit-output/evidence/differential-inputs.jsonl")
ALPHABET = "0123456789ABCDEF"
EXAMPLES = ("AB", "1077E", "ABED1A33", "123456789ABCDEF0", "2020")
BOUNDARIES = (
    "",
    *(ALPHABET),
    "2",
    "3",
    "5",
    "7",
    "B",
    "D",
    "0",
    "1",
    "4",
    "6",
    "8",
    "9",
    "A",
    "C",
    "E",
    "F",
    ALPHABET,
    ALPHABET[::-1],
    "2357BD",
    "014689ACEF",
    "2" * 1000,
    "F" * 1000,
    ("2F" * 500),
)


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


canonical = load_function("trusted_canonical", CANONICAL_PATH)
candidate = load_function("generated_solution", CANDIDATE_PATH)

tagged_inputs: list[tuple[str, str]] = []
tagged_inputs.extend(("example", value) for value in EXAMPLES)
tagged_inputs.extend(("boundary", value) for value in BOUNDARIES)
for length in range(5):
    tagged_inputs.extend(
        ("exhaustive_length_le_4", "".join(chars))
        for chars in itertools.product(ALPHABET, repeat=length)
    )

rng = random.Random(780078)
for _ in range(2000):
    length = rng.randrange(0, 257)
    tagged_inputs.append(
        ("deterministic_random_length_0_256", "".join(rng.choices(ALPHABET, k=length)))
    )

# Keep the first scope tag for duplicate values while retaining every unique input.
unique_inputs: dict[str, str] = {}
for scope, value in tagged_inputs:
    unique_inputs.setdefault(value, scope)

mismatches: list[dict[str, object]] = []
digest = hashlib.sha256()
with INPUT_LOG.open("w", encoding="utf-8") as stream:
    for value, scope in unique_inputs.items():
        expected = canonical(value)
        actual = candidate(value)
        record = {
            "scope": scope,
            "input": value,
            "canonical": expected,
            "candidate": actual,
        }
        serialized = json.dumps(record, sort_keys=True, separators=(",", ":"))
        stream.write(serialized + "\n")
        digest.update((serialized + "\n").encode())
        if expected != actual:
            mismatches.append(record)

print(f"canonical={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"domain_alphabet={ALPHABET!r}")
print("documented_examples=5")
print("branch_boundary_singletons=all 16 hexadecimal symbols")
print("exhaustive_scope=all uppercase hexadecimal strings of length 0 through 4")
print("random_scope=2000 deterministic strings with lengths 0 through 256")
print(f"unique_inputs={len(unique_inputs)}")
print(f"input_log={INPUT_LOG}")
print(f"input_log_sha256={digest.hexdigest()}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH " + json.dumps(mismatch, sort_keys=True))

if mismatches:
    raise SystemExit(1)
