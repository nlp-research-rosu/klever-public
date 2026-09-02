#!/usr/bin/env python3
"""Independent candidate-vs-trusted-reference differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/candidate/solution.py"), "candidate_solution")

# The trusted prompt's intended domain is all positive integers. The prompt has
# no embedded examples, so 1, 2, 3, and 5 cover the branch boundary and the
# conventional small examples present in candidate evidence.
fixed_inputs = [1, 2, 3, 4, 5, 9, 10, 25, 100, 250, 512]
rng = random.Random(8301)
generated_inputs = [rng.randint(1, 512) for _ in range(200)]
inputs = fixed_inputs + generated_inputs

mismatches: list[tuple[int, object, object]] = []
for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected or type(actual) is not type(expected):
        mismatches.append((n, expected, actual))

print(f"intended_domain_cases={len(inputs)}")
print(f"fixed_inputs={fixed_inputs}")
print(f"generated_seed=8301 generated_count={len(generated_inputs)} range=[1,512]")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for row in mismatches[:20]:
        print(f"mismatch={row!r}")
    raise SystemExit(1)

# Independently enumerate the actual natural-language counting property for
# tractable digit lengths. This oracle does not reuse the closed-form formula.
def brute_count(n: int) -> int:
    lower = 1 if n == 1 else 10 ** (n - 1)
    upper = 10**n
    return sum(
        1
        for value in range(lower, upper)
        if str(value).startswith("1") or str(value).endswith("1")
    )


brute_inputs = [1, 2, 3, 4, 5]
brute_rows = [
    (n, brute_count(n), canonical(n), candidate(n)) for n in brute_inputs
]
print(f"brute_rows={brute_rows}")
if any(brute != expected or brute != actual for _, brute, expected, actual in brute_rows):
    raise SystemExit(1)

# Ground substitutions into the two K postconditions: n=1 uses the first claim;
# every n>=2 uses 18 * 10 ** (n - 2).
ground_inputs = [1, 2, 7, 10]
ground_rows = []
for n in ground_inputs:
    claimed = 1 if n == 1 else 18 * 10 ** (n - 2)
    ground_rows.append((n, claimed, canonical(n), candidate(n)))
print(f"ground_claim_rows={ground_rows}")
if any(claimed != expected or claimed != actual for _, claimed, expected, actual in ground_rows):
    raise SystemExit(1)

# There is no "empty" scalar integer in the intended domain. As an excluded
# robustness probe, verify that omitting the argument raises the same exception
# class in both implementations. This is not evidence about the formal theorem.
excluded_exceptions = []
for label, fn in (("canonical", canonical), ("candidate", candidate)):
    try:
        fn()
    except Exception as err:  # noqa: BLE001 - deliberate exception comparison
        excluded_exceptions.append((label, type(err).__name__))
    else:
        excluded_exceptions.append((label, "NO_EXCEPTION"))
print(f"excluded_empty_call={excluded_exceptions}")
if [kind for _, kind in excluded_exceptions] != ["TypeError", "TypeError"]:
    raise SystemExit(1)

print("RESULT: PASS")
