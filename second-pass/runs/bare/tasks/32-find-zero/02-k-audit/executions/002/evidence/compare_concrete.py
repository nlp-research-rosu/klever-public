#!/usr/bin/env python3
"""Compare recorded K rational results with independent Python execution."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import re


solution_path = Path("/tmp/audit-work/32-find-zero/solution.py")
module_spec = importlib.util.spec_from_file_location("generated_solution", solution_path)
assert module_spec is not None and module_spec.loader is not None
solution = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(solution)

cases = {
    "linear": [1, 2],
    "empty": [],
    "zero": [0, 1],
    "expansion": [-8, 0, 0, 1],
    "endpoint": [1, 1],
}

pattern = re.compile(r"rat \( (-?\d+) , (\d+) \)")
for name, coefficients in cases.items():
    log_path = Path(f"/audit-output/evidence/stage3-krun-haskell-{name}.log")
    log_text = log_path.read_text(encoding="utf-8")
    match = pattern.search(log_text)
    assert match is not None, log_path
    k_result = Fraction(int(match.group(1)), int(match.group(2)))
    python_float = solution.find_zero(coefficients)
    python_result = Fraction.from_float(python_float)
    print(
        f"{name}: xs={coefficients} "
        f"K={k_result.numerator}/{k_result.denominator} "
        f"Python={python_result.numerator}/{python_result.denominator} "
        f"float={python_float:.17g} equal={k_result == python_result}"
    )
    assert k_result == python_result

print("CONCRETE_COMPARISON_OK")
