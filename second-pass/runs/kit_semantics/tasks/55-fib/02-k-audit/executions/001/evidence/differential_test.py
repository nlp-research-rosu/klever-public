#!/usr/bin/env python3
"""Independent candidate-versus-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/fib-audit")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_module("generated_solution", SCRATCH / "solution.py")

documented = [10, 1, 8]
boundaries = [0, 1, 2]
rng = random.Random(55)
generated = [rng.randrange(0, 35) for _ in range(24)]
cases = list(dict.fromkeys(documented + boundaries + list(range(0, 31)) + generated))

mismatches = []
rows = []
for n in cases:
    expected = canonical.fib(n)
    actual = candidate.fib(n)
    rows.append((n, expected, actual))
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"documented={documented}")
print(f"boundaries={boundaries}")
print(f"generated_seed=55 generated={generated}")
print(f"unique_intended_cases={cases}")
print(f"rows={rows}")
print(f"mismatches={len(mismatches)} {mismatches}")

# Negative integers are recorded as an explicit domain probe.  They do not
# denote a natural-number Fibonacci index; the trusted recursive reference
# raises RecursionError while the candidate loop returns 0.
for n in (-1, -5):
    actual = candidate.fib(n)
    try:
        expected = canonical.fib(n)
    except Exception as error:  # exact exception class is evidence
        expected = f"{type(error).__name__}: {error}"
    print(f"out_of_domain n={n} canonical={expected!r} candidate={actual!r}")

if mismatches:
    raise SystemExit(1)
