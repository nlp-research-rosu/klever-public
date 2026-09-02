#!/usr/bin/env python3
"""Independent differential test for HumanEval 46.

The trusted canonical implementation and submitted implementation are imported
from separate files.  Test inputs are selected here and do not reuse K claims
or proof equations.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import random


SCRATCH = Path("/tmp/audit-work/46-fib4-review")


def load_function(module_name: str, path: Path):
    spec = spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_function("submitted_solution", SCRATCH / "solution.py")

documented = [5, 6, 7]
branch_boundaries = [0, 1, 2, 3, 4]
exhaustive_small = list(range(0, 201))
rng = random.Random(460046)
generated = [rng.randint(201, 2000) for _ in range(100)]
intended_cases = sorted(set(documented + branch_boundaries + exhaustive_small + generated))

mismatches = []
for n in intended_cases:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        mismatches.append((n, expected, actual))

print("contract_domain=nonnegative integers (n-th sequence element)")
print("empty_case=not applicable to an integer argument")
print(f"documented_examples={documented}")
print(f"branch_boundaries={branch_boundaries}")
print("generated_seed=460046")
print(f"generated_draws={len(generated)} range=[201,2000]")
print(f"unique_intended_cases={len(intended_cases)}")
print(f"mismatch_count={len(mismatches)}")
print(f"mismatches={mismatches}")
for n in [0, 1, 2, 3, 4, 5, 6, 7, 12, 50, 200, 1000, 2000]:
    value = candidate(n)
    print(f"sample n={n} value={value} decimal_digits={len(str(value))}")

print("outside_domain_negative_probe:")
for n in [-1, -2, -3, -4]:
    observations = []
    for name, function in [("canonical", canonical), ("candidate", candidate)]:
        try:
            observations.append((name, "value", function(n)))
        except Exception as error:
            observations.append((name, "exception", type(error).__name__))
    print(f"n={n} observations={observations}")

raise SystemExit(1 if mismatches else 0)
