#!/usr/bin/env python3
"""Mechanically inventory the two submitted claims and check fixed results."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/46-fib4-review")
spec_text = (ROOT / "spec.k").read_text()


def load_function(module_name: str, path: Path):
    spec = spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


labels = re.findall(r"claim\s+\[([^\]]+)\]", spec_text)
claim_requires = re.findall(r"(?m)^\s+requires\s", spec_text)
assertions = [
    (int(n), int(expected))
    for n, expected in re.findall(
        r'Call\(Name\("fib4"\),\s*Int\((\d+)\)\)\s*,\s*'
        r'CmpOp\("=="\s*,\s*Int\((\d+)\)\)',
        spec_text,
    )
]
canonical = load_function("scope_canonical", ROOT / "canonical.py")
candidate = load_function("scope_candidate", ROOT / "solution.py")
fixed_checks = [
    (n, expected, canonical(n), candidate(n))
    for n, expected in assertions
]

print(f"claim_labels={labels}")
print(f"claim_requires_clause_count={len(claim_requires)}")
print(f"operational_fixed_assertions={len(assertions)}")
print(f"operational_input_min={min(n for n, _ in assertions)}")
print(f"operational_input_max={max(n for n, _ in assertions)}")
print(f"operational_inputs={[n for n, _ in assertions]}")
print(f"fixed_checks={fixed_checks}")
print(
    "fixed_check_mismatches="
    + str(
        [
            item
            for item in fixed_checks
            if not (item[1] == item[2] == item[3])
        ]
    )
)
print(
    "loop_step_witness="
    + str(
        {
            "before": {
                "a": 0,
                "b": 0,
                "c": 2,
                "d": 0,
                "next_value": 999,
                "i": 4,
            },
            "after": {
                "a": 0,
                "b": 2,
                "c": 0,
                "d": 2,
                "next_value": 2,
                "i": 5,
            },
        }
    )
)
