#!/usr/bin/env python3
"""Independent candidate-vs-canonical and contract differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


canonical = load_function("trusted_canonical", "/tmp/audit-work/python-tests/canonical.py")
candidate = load_function(
    "generated_solution", "/tmp/audit-work/python-tests/generated_solution.py"
)


def contract_oracle(s: str) -> str:
    if any(ch.isalpha() for ch in s):
        return "".join(ch.swapcase() for ch in s)
    return s[::-1]


documented = {
    "1234": "4321",
    "ab": "AB",
    "#a@C": "#A@c",
}

boundary = [
    "",
    "0",
    "#",
    "12#",
    "A",
    "Z",
    "a",
    "z",
    "@A[",
    "`a{",
    "AaZz",
    "0A!",
    "é",
    "É",
    "Ωω",
    "ΟΣ",
    "AΣ",
    "ΣΣ",
    "ΜΆΙΟΣ",
    "ß",
    "İı",
    "ǅ",
    "α1#",
    "中",
    "１２",
    "🙂1#",
    "e\u0301",
    "\u0301",
    "\x00",
    "\n\t",
]

alphabet = ["A", "z", "0", "#", "é", "Ω", "ß", "中", "🙂", "\u0301"]
exhaustive = [
    "".join(chars)
    for size in range(0, 4)
    for chars in itertools.product(alphabet, repeat=size)
]

rng = random.Random(161)
pool = alphabet + ["b", "Y", "9", " ", "\n", "İ", "ı", "ǅ", "𝔄"]
generated = [
    "".join(rng.choice(pool) for _ in range(rng.randrange(0, 18)))
    for _ in range(2000)
]

cases = list(dict.fromkeys([*documented, *boundary, *exhaustive, *generated]))
mismatches = []
for s in cases:
    ref = canonical(s)
    got = candidate(s)
    oracle = contract_oracle(s)
    if ref != got or ref != oracle:
        mismatches.append((s, ref, got, oracle))

for s, expected in documented.items():
    actual = candidate(s)
    if actual != expected:
        mismatches.append((s, expected, actual, "documented example"))

print("canonical_path=/tmp/audit-work/python-tests/canonical.py")
print("candidate_path=/tmp/audit-work/python-tests/generated_solution.py")
print("oracle=independent direct transcription of prompt using Python isalpha/swapcase")
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundary)}")
print(f"exhaustive_alphabet={alphabet!r}")
print("exhaustive_lengths=0..3")
print(f"fixed_seed_generated_cases={len(generated)} seed=161 max_length=17")
print(f"unique_total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))

unicode_witnesses = ["é", "Ωω", "ß", "İı", "ǅ", "中"]
for s in unicode_witnesses:
    print(
        "UNICODE",
        repr(s),
        "canonical=",
        repr(canonical(s)),
        "candidate=",
        repr(candidate(s)),
    )

raise SystemExit(1 if mismatches else 0)
