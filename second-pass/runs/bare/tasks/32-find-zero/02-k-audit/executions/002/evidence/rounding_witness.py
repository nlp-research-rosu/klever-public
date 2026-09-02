#!/usr/bin/env python3
"""Intended-domain witness that exact-rational K diverges from Python floats."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import re


spec = importlib.util.spec_from_file_location(
    "generated_solution", "/tmp/audit-work/32-find-zero/solution.py"
)
assert spec is not None and spec.loader is not None
solution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution)

coefficients = [2**53 + 1, -(2**54)]
python_at_zero = solution.evaluate_polynomial(coefficients, 0.0)
python_at_half = solution.evaluate_polynomial(coefficients, 0.5)
exact_at_zero = Fraction(coefficients[0])
exact_at_half = Fraction(coefficients[0]) + Fraction(coefficients[1], 2)
python_branch = python_at_half * python_at_zero > 0
exact_branch = exact_at_half * exact_at_zero > 0
python_root = solution.find_zero(coefficients)

k_log = Path(
    "/audit-output/evidence/stage5-rounding-witness-krun.log"
).read_text(encoding="utf-8")
match = re.search(r"rat \( (-?\d+) , (\d+) \)", k_log)
assert match is not None
k_root = Fraction(int(match.group(1)), int(match.group(2)))

print(f"coefficients={coefficients}")
print(f"domain_valid_even_length={len(coefficients) % 2 == 0}")
print(f"domain_valid_nonzero_highest={coefficients[-1] != 0}")
print(f"python_p(0)={python_at_zero!r}")
print(f"exact_p(0)={exact_at_zero}")
print(f"python_p(1/2)={python_at_half!r}")
print(f"exact_p(1/2)={exact_at_half}")
print(f"python_branch_product_gt_zero={python_branch}")
print(f"exact_K_branch_product_gt_zero={exact_branch}")
print(
    f"python_root={python_root!r} "
    f"as_fraction={Fraction.from_float(python_root)}"
)
print(f"K_root={k_root}")
print(f"root_results_equal={Fraction.from_float(python_root) == k_root}")

assert not python_branch
assert exact_branch
assert Fraction.from_float(python_root) != k_root
print("ROUNDING_DIVERGENCE_CONFIRMED")
