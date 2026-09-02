#!/usr/bin/env python3
"""Satisfying witnesses and concrete substitutions for every entry claim."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(Path("/tmp/audit-work/reconstruction/solution.py"), "generated_witness")

claims = [
    ("universal", 8, lambda n: True, lambda n: n >= 8 and n % 2 == 0),
    ("even-at-least-eight", 10, lambda n: n >= 8 and n % 2 == 0, lambda n: True),
    ("below-eight", 7, lambda n: n < 8, lambda n: False),
    ("odd-at-least-eight", 9, lambda n: n >= 8 and n % 2 != 0, lambda n: False),
]

failures = 0
for name, n, precondition, claimed_result in claims:
    pre = precondition(n)
    post = claimed_result(n)
    can = canonical.is_equal_to_sum_even(n)
    gen = generated.is_equal_to_sum_even(n)
    passed = pre and post == can == gen
    failures += not passed
    print(
        f"claim={name} witness={n} precondition={pre} "
        f"claimed_result={post} canonical={can} generated={gen} "
        f"status={'PASS' if passed else 'FAIL'}"
    )

for n in [8, 10, 100]:
    terms = (2, 2, 2, n - 6)
    passed = all(x > 0 and x % 2 == 0 for x in terms) and sum(terms) == n
    failures += not passed
    print(f"constructive_contract_witness n={n} terms={terms} status={'PASS' if passed else 'FAIL'}")

print(f"OVERALL: {'PASS' if failures == 0 else 'FAIL'}")
sys.exit(1 if failures else 0)
