#!/usr/bin/env python3
"""Independent differential test for HumanEval 139-special-factorial."""

from __future__ import annotations

import hashlib
import importlib.util
import math
from pathlib import Path
import random


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_factorial


def independent_oracle(n: int) -> int:
    return math.prod(math.factorial(k) for k in range(1, n + 1))


def render(value: int) -> str:
    text = str(value)
    if len(text) <= 80:
        return text
    digest = hashlib.sha256(text.encode()).hexdigest()
    return f"<digits={len(text)} sha256={digest}>"


def main() -> None:
    canonical = load_entry(
        "trusted_humaneval_139", Path("/reference/canonical.py")
    )
    generated = load_entry(
        "candidate_humaneval_139", Path("/tmp/audit-work/case/solution.py")
    )

    # Documented n=4, the n>0 lower boundary, the loop's no-iteration
    # robustness boundary n=0, negative out-of-contract cases, small
    # progression values, and larger deterministic values.
    fixed = [-3, -1, 0, 1, 2, 3, 4, 5, 6, 10, 20, 30]
    rng = random.Random(139)
    generated_inputs = [rng.randint(1, 60) for _ in range(100)]
    inputs = fixed + generated_inputs

    intended_mismatches = []
    robustness_mismatches = []
    for index, n in enumerate(inputs):
        expected = canonical(n)
        actual = generated(n)
        oracle = independent_oracle(n)
        category = "intended" if n > 0 else "out-of-contract"
        print(
            f"case={index:03d} n={n} category={category} "
            f"canonical={render(expected)} generated={render(actual)} "
            f"oracle={render(oracle)}"
        )
        mismatch = expected != actual or expected != oracle
        if mismatch and n > 0:
            intended_mismatches.append((n, expected, actual, oracle))
        elif mismatch:
            robustness_mismatches.append((n, expected, actual, oracle))

    print(f"fixed_inputs={fixed}")
    print(f"random_seed=139 random_count={len(generated_inputs)}")
    print(f"random_inputs={generated_inputs}")
    print(f"intended_domain_cases={sum(n > 0 for n in inputs)}")
    print(f"intended_domain_mismatches={len(intended_mismatches)}")
    print(f"out_of_contract_cases={sum(n <= 0 for n in inputs)}")
    print(f"out_of_contract_mismatches={len(robustness_mismatches)}")
    if intended_mismatches:
        raise AssertionError(intended_mismatches)


if __name__ == "__main__":
    main()
