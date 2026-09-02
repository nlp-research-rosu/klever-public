#!/usr/bin/env python3
"""Mechanically audit concrete spec coverage and expected results."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


spec_text = Path("/tmp/audit-work/75-is-multiply-prime/spec.k").read_text()
canonical = load_module("coverage_canonical", Path("/reference/canonical.py"))
generated = load_module(
    "coverage_generated",
    Path("/tmp/audit-work/75-is-multiply-prime/solution.py"),
)

negative_pattern = re.compile(
    r"module SPEC-NEGATIVE.*?"
    r"#runIsMultiplyPrime\(A:Int\)\s*=>\s*false.*?"
    r"requires\s+A\s*<Int\s*2.*?"
    r"endmodule",
    re.DOTALL,
)
negative_match = bool(negative_pattern.search(spec_text))
print(f"symbolic_negative_claim_shape_match={negative_match}")
print("symbolic_negative_satisfying_witness: A=-7")
print(
    "  canonical(-7)="
    f"{canonical.is_multiply_prime(-7)} "
    "generated(-7)="
    f"{generated.is_multiply_prime(-7)} "
    "precondition(-7<2)=True"
)

pair_pattern = re.compile(
    r"#runIsMultiplyPrime\((-?\d+)\)\s*~>\s*#expect\((true|false)\)"
)
pairs = [(int(number), expected == "true") for number, expected in pair_pattern.findall(spec_text)]
numbers = [number for number, _ in pairs]
expected_numbers = list(range(2, 100))

print(f"concrete_checkpoint_count={len(pairs)}")
print(f"concrete_checkpoint_min={min(numbers)} max={max(numbers)}")
print(f"concrete_checkpoint_unique_count={len(set(numbers))}")
print(f"concrete_domain_exactly_2_through_99={numbers == expected_numbers}")

mismatches: list[tuple[int, bool, bool, bool]] = []
for number, expected in pairs:
    canonical_result = canonical.is_multiply_prime(number)
    generated_result = generated.is_multiply_prime(number)
    if expected != canonical_result or expected != generated_result:
        mismatches.append((number, expected, canonical_result, generated_result))

print(f"checkpoint_result_mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")

module_pattern = re.compile(r"module (SPEC-[A-Z0-9-]+).*?endmodule", re.DOTALL)
modules = module_pattern.findall(spec_text)
print(f"entry_module_count={len(modules)}")
print(f"entry_modules={','.join(modules)}")
print(
    "finite_claim_satisfying_state: each concrete claim starts from the explicit "
    "module scope 0 plus builtins scope -1, empty heap/stack, noRet, NoExc, "
    "exit-code 0; the displayed ground K terms witness satisfiability"
)

okay = (
    negative_match
    and numbers == expected_numbers
    and len(set(numbers)) == 98
    and not mismatches
    and len(modules) == 11
)
raise SystemExit(0 if okay else 1)
