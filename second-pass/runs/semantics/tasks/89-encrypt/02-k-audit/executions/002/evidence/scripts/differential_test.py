#!/usr/bin/env python3
"""Independent differential test for HumanEval/89 encrypt."""

from __future__ import annotations

import importlib.util
import random
import string
from pathlib import Path


def load_encrypt(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


canonical = load_encrypt("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_encrypt("candidate_solution", Path("/candidate/solution.py"))

documented = ["hi", "asdfghjkl", "gf", "et"]
boundaries = [
    "",
    "a",
    "v",
    "w",
    "x",
    "y",
    "z",
    "abcdefghijklmnopqrstuvwxyz",
    "`",
    "{",
    "A",
    "Z",
    "0",
    "9",
    " ",
    "\n",
    "\x00",
    "\x7f",
    "aZ-9z",
    "\u00e9",
    "\U0010ffff",
]

rng = random.Random(8904)
alphabet = string.ascii_letters + string.digits + string.punctuation + " \t\n"
generated = [
    "".join(rng.choice(alphabet) for _ in range(length))
    for length in range(0, 65)
]

cases = documented + boundaries + generated
mismatches: list[tuple[int, str, str, str]] = []
for index, value in enumerate(cases):
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append((index, value, expected, actual))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"seeded_generated_cases={len(generated)} seed=8904")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for index, value, expected, actual in mismatches[:20]:
    print(
        f"mismatch[{index}] input={value!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )

if mismatches:
    raise SystemExit(1)
