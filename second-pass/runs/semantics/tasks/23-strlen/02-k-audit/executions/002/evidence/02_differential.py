#!/usr/bin/env python3
"""Independent differential test for HumanEval/23."""

from __future__ import annotations

import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    # Compile the audited source bytes directly so an adjacent untrusted .pyc
    # cannot satisfy the import.
    namespace = {"__name__": module_name, "__file__": str(path)}
    source = path.read_text(encoding="utf-8")
    exec(compile(source, str(path), "exec"), namespace)
    return namespace["strlen"]


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("candidate_solution", Path("/candidate/solution.py"))

documented = ["", "abc"]
boundaries = [
    "a",
    "\0",
    "\n",
    "é",
    "e\u0301",
    "🙂",
    "\ud800",
    "a" * 255,
    "b" * 256,
    "c" * 4096,
]

rng = random.Random(230023)
alphabet = ["a", "Z", "0", " ", "\0", "\n", "é", "\u0301", "🙂", "\ud800"]
generated_inputs = []
for _ in range(500):
    length = rng.randrange(0, 129)
    generated_inputs.append("".join(rng.choice(alphabet) for _ in range(length)))

cases = documented + boundaries + generated_inputs
mismatches = []
for index, value in enumerate(cases):
    expected = canonical(value)
    actual = generated(value)
    if expected != actual:
        mismatches.append((index, repr(value), expected, actual))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"generated_cases={len(generated_inputs)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
print(f"sample_results={[generated(x) for x in documented + boundaries[:6]]}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch}")
    raise SystemExit(1)
print("DIFFERENTIAL_CHECK=PASS")
