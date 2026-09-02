#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/56."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
candidate = load_entry(Path("/tmp/audit-work/proof/solution.py"), "candidate_solution")

documented = {
    "<": False,
    "<>": True,
    "<<><>>": True,
    "><<>": False,
}

branch_and_boundary = [
    "",
    ">",
    "<<",
    ">>",
    "><",
    "<><>",
    "<<>>",
    "<>>",
    "<<<>>>",
    "<<>><>",
    "><><",
    ">>>>",
    "<<<<",
]

tests = set(documented)
tests.update(branch_and_boundary)

# Exhaust every word through length 12 (all loop/branch boundaries in small cases).
for length in range(13):
    tests.update("".join(chars) for chars in itertools.product("<>", repeat=length))

# Broader deterministic finite evidence, including long unbalanced and balanced inputs.
rng = random.Random(560056)
for _ in range(500):
    length = rng.randrange(0, 257)
    tests.add("".join(rng.choice("<>") for _ in range(length)))
for pairs in (1, 2, 8, 32, 128, 512):
    tests.add("<" * pairs + ">" * pairs)
    tests.add("<>" * pairs)
    tests.add(">" + "<" * pairs + ">" * max(0, pairs - 1))

mismatches = []
for text in sorted(tests, key=lambda value: (len(value), value)):
    expected = canonical(text)
    actual = candidate(text)
    if text in documented and expected != documented[text]:
        mismatches.append(("trusted-example", text, documented[text], expected))
    if actual != expected:
        mismatches.append(("candidate", text, expected, actual))

print(f"documented_examples={len(documented)}")
print(f"boundary_cases={len(branch_and_boundary)}")
print("exhaustive_lengths=0..12")
print("random_seed=560056 random_cases=500 max_random_length=256")
print(f"unique_cases={len(tests)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(repr(mismatch))

sys.exit(1 if mismatches else 0)
