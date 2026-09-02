#!/usr/bin/env python3
"""Independent differential check for HumanEval 28 on the intended list[str] domain."""

from __future__ import annotations

import importlib.util
import random
import string
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.concatenate


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("candidate_solution", Path("/candidate/solution.py"))

documented_and_boundaries = [
    [],
    [""],
    ["a"],
    ["a", "b", "c"],
    ["", ""],
    ["", "hello", "", " world"],
    ["left", "", "right"],
    [" ", "\t", "\n"],
    ["é", "λ", "🙂"],
    ["a\x00b", "\x00", "c"],
    ['"', "\\", "\r\n"],
    ["x" * 1024],
    ["a"] * 1000,
]

rng = random.Random(280028)
alphabet = string.ascii_letters + string.digits + " \t\n-_éλ🙂\x00"
generated_inputs: list[list[str]] = []
for list_length in range(0, 33):
    for _ in range(16):
        values = []
        for _item in range(list_length):
            length = rng.randrange(0, 33)
            values.append("".join(rng.choice(alphabet) for _ in range(length)))
        generated_inputs.append(values)

cases = documented_and_boundaries + generated_inputs
mismatches = []
for index, value in enumerate(cases):
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append((index, value, expected, actual))

print("oracle=/reference/canonical.py:concatenate")
print("candidate=/candidate/solution.py:concatenate")
print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
for index, value in enumerate(documented_and_boundaries):
    print(
        f"boundary[{index}] input={value!r} "
        f"result={generated(value)!r}"
    )
print("random_seed=280028")
print("generated_length_range=0..32")
print("generated_samples_per_length=16")
print(f"generated_cases={len(generated_inputs)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
