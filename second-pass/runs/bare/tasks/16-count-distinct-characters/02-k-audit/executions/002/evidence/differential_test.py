#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/16."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


canonical = load_function(
    Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical"
)
candidate = load_function(
    Path("/tmp/audit-work/source/solution.py"), "generated_solution"
)

documented_and_boundary_cases = [
    "xyzXYZ",
    "Jerry",
    "",
    "a",
    "A",
    "aA",
    "AaBb!",
    "0123456789",
    " \t\n",
    "Ää",
    "Αα",
    "Σσς",
    "İi",
    "ßẞ",
    "éÉeE",
    "e\u0301É",
    "😀😀A",
    "\x00A\x00a",
]

rng = random.Random(160016)
alphabet = (
    "abABxyzXYZ019 !\t\n"
    "ÄäÖöÜüÉé"
    "ΑαΒβΣσς"
    "İıIißẞ"
    "e\u0301"
    "😀🐍"
)
generated_cases = [
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 33)))
    for _ in range(2000)
]

mismatches = []
for index, value in enumerate(documented_and_boundary_cases + generated_cases):
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append((index, value, expected, actual))

print(f"fixed_cases={len(documented_and_boundary_cases)}")
for value in documented_and_boundary_cases:
    print(
        "case="
        f"{value!r} canonical={canonical(value)} candidate={candidate(value)}"
    )
print(f"generated_cases={len(generated_cases)} seed=160016")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"mismatch={mismatch!r}")
    raise SystemExit(1)
