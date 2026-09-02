#!/usr/bin/env python3
"""Concrete witness that candidate K decimal-float semantics is not CPython float."""

from fractions import Fraction
import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


value = 3.7
numerator, denominator = value.as_integer_ratio()
exact_binary_value = Fraction(numerator, denominator)
exact_decimal_threshold = Fraction(37, 10)
canonical = load_function("canonical_witness", Path("/tmp/audit-work/canonical.py"))
candidate = load_function(
    "candidate_witness", Path("/tmp/audit-work/reconstruction/solution.py")
)

print(f"python_input={value!r}")
print(f"python_input_as_integer_ratio=({numerator},{denominator})")
print(f"exact_binary_value_minus_37_over_10={exact_binary_value - exact_decimal_threshold}")
print(f"python_input_gt_float_literal_3_7={value > 3.7}")
print(f"canonical_result={canonical([value])!r}")
print(f"candidate_python_result={candidate([value])!r}")
print("candidate_K_result_for_same_ratio='A' (see stage3-krun-ieee-3.7-witness.log)")

assert exact_binary_value > exact_decimal_threshold
assert not (value > 3.7)
assert canonical([value]) == ["A-"]
assert candidate([value]) == ["A-"]
print("IEEE_BRIDGE_WITNESS: K='A' versus both Python implementations='A-'")
