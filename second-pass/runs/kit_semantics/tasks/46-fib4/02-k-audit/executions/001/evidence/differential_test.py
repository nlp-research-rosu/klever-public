#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/46-fib4")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


def recurrence_oracle(n: int) -> int:
    """Direct prompt recurrence with a stored prefix; defined for n >= 0."""
    values = [0, 0, 2, 0]
    for index in range(4, n + 1):
        values.append(sum(values[index - 4 : index]))
    return values[n]


def main() -> int:
    canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical")
    candidate = load_function(SCRATCH / "solution.py", "generated_solution")

    documented = {5: 4, 6: 8, 7: 14}
    boundary = [0, 1, 2, 3, 4, 5]
    exhaustive_small = list(range(0, 65))
    rng = random.Random(46004)
    generated = [rng.randrange(0, 501) for _ in range(100)]
    inputs = sorted(set(boundary + list(documented) + exhaustive_small + generated))

    mismatches: list[tuple[int, object, object, object]] = []
    for n in inputs:
        expected = recurrence_oracle(n)
        canonical_value = canonical(n)
        candidate_value = candidate(n)
        if canonical_value != expected or candidate_value != expected:
            mismatches.append((n, canonical_value, candidate_value, expected))

    documented_failures = [
        (n, candidate(n), expected)
        for n, expected in documented.items()
        if candidate(n) != expected
    ]

    print("contract_domain: nonnegative integer sequence indices")
    print("empty_case: not applicable to scalar input; n=0 is the zero-iteration case")
    print(f"branch_boundaries: {boundary}")
    print(f"documented_examples: {documented}")
    print("generated_seed: 46004")
    print("generated_range: [0, 500], draws=100")
    print("exhaustive_small: [0, 64]")
    print(f"unique_inputs_tested: {len(inputs)}")
    print(f"largest_input: {max(inputs)}")
    print(f"documented_failures: {documented_failures}")
    print(f"mismatches: {len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(f"MISMATCH {mismatch}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
