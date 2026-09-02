#!/usr/bin/env python3
"""Independent differential check for HumanEval 103.

The exact-contract oracle uses Fraction and its own half-even rounding helper;
it does not import or reuse the generated implementation.
"""

from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import random
import hashlib


def load_entry(path: str, module_name: str):
    spec = spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
generated = load_entry("/candidate/solution.py", "generated_solution")


def round_half_even(value: Fraction) -> int:
    lower = value.numerator // value.denominator
    remainder = value - lower
    if remainder < Fraction(1, 2):
        return lower
    if remainder > Fraction(1, 2):
        return lower + 1
    return lower if lower % 2 == 0 else lower + 1


def exact_contract(n: int, m: int):
    if n > m:
        return -1
    return bin(round_half_even(Fraction(n + m, 2)))


documented_and_boundaries = [
    (1, 5),      # documented, integral mean
    (7, 5),      # documented, inverted/empty interval
    (10, 20),    # documented
    (20, 33),    # documented, half-even down
    (1, 1),      # smallest valid singleton
    (2, 1),      # branch boundary immediately above m
    (1, 2),      # half-even up: lower neighbor odd
    (2, 3),      # half-even down: lower neighbor even
    (3, 4),      # half-even up
    (4, 5),      # half-even down
    (5, 5),      # odd singleton
    (6, 6),      # even singleton
]

rng = random.Random(103)
generated_inputs = []
for _ in range(5000):
    base = rng.randint(1, 10**12)
    delta = rng.randint(-5, 20)
    generated_inputs.append((base, max(1, base + delta)))

# These expose the trusted canonical implementation's float-conversion
# limitation while the generated integer formulation remains exact.
large_boundaries = [
    (2**53 - 1, 2**53 - 1),
    (2**53, 2**53),
    (2**53 + 1, 2**53 + 1),
    (2**54 + 1, 2**54 + 1),
    (10**100, 10**100),
    (10**309, 10**309),
]

cases = list(documented_and_boundaries)
cases += [(n, m) for n in range(1, 201) for m in range(1, 201)]
cases += generated_inputs
cases += large_boundaries

generated_exact_mismatches = []
canonical_exact_mismatches = []
canonical_exceptions = []
for n, m in cases:
    expected = exact_contract(n, m)
    actual = generated(n, m)
    if actual != expected:
        generated_exact_mismatches.append((n, m, actual, expected))
    try:
        reference = canonical(n, m)
    except Exception as err:  # record, do not hide canonical domain failures
        canonical_exceptions.append((n, m, type(err).__name__, str(err)))
    else:
        if reference != expected:
            canonical_exact_mismatches.append((n, m, reference, expected))

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print("small_exhaustive_cases=40000 domain=n,m in [1,200]")
print(f"seeded_generated_cases={len(generated_inputs)} seed=103")
print(f"large_boundary_cases={len(large_boundaries)}")
print(f"total_cases={len(cases)}")
print(f"generated_vs_exact_mismatches={len(generated_exact_mismatches)}")
print(f"canonical_vs_exact_mismatches={len(canonical_exact_mismatches)}")
print(f"canonical_exceptions={len(canonical_exceptions)}")


def compact(value) -> str:
    text = str(value)
    digest = hashlib.sha256(text.encode()).hexdigest()[:16]
    if len(text) <= 80:
        return repr(value)
    return f"<len={len(text)} sha256[:16]={digest} prefix={text[:32]!r}>"


for row in canonical_exact_mismatches[:10]:
    print("canonical_mismatch", *(compact(value) for value in row))
for row in canonical_exceptions[:10]:
    print("canonical_exception", *(compact(value) for value in row))

if generated_exact_mismatches:
    for row in generated_exact_mismatches[:10]:
        print("generated_mismatch", *(compact(value) for value in row))
    raise SystemExit(1)
