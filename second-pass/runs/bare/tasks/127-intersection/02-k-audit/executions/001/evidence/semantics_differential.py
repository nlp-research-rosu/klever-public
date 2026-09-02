#!/usr/bin/env python3
"""Compare fresh K execution with the trusted Python oracle on boundary cases."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


ROOT = Path("/tmp/audit-work/127-intersection")
RUN = ROOT / "run"
canonical = load_entry(ROOT / "trusted" / "canonical.py")

cases = [
    ("example_touch", (1, 2), (2, 3)),
    ("example_length_one", (-1, 1), (0, 4)),
    ("example_prime_two", (-3, -1), (-5, 5)),
    ("disjoint", (0, 1), (3, 4)),
    ("singletons", (0, 0), (0, 0)),
    ("left_equal_right_second", (0, 8), (0, 5)),
    ("left_second_right_equal", (0, 8), (2, 8)),
    ("left_first_right_first", (2, 7), (0, 8)),
    ("length_two", (0, 2), (0, 2)),
    ("length_three", (0, 3), (0, 3)),
    ("length_four", (0, 4), (0, 4)),
    ("length_five", (0, 5), (0, 5)),
    ("length_six", (0, 6), (0, 6)),
    ("length_nine", (0, 9), (0, 9)),
    ("length_25", (0, 25), (0, 25)),
    ("negative_endpoints_prime", (-100, -3), (-200, 0)),
]

result_pattern = re.compile(r'strVal\s*\(\s*"(YES|NO)"\s*\)')
mismatches = []

for label, first, second in cases:
    first_term = f"TupleExpr(Int({first[0]}),Int({first[1]}))"
    second_term = f"TupleExpr(Int({second[0]}),Int({second[1]}))"
    command = [
        "krun",
        str(RUN / "solution.mpy"),
        "--definition",
        str(RUN / "semantic-fresh-kompiled"),
        f"-cINTERVAL1={first_term}",
        f"-cINTERVAL2={second_term}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command, cwd=RUN, check=False, text=True, capture_output=True
    )
    combined = completed.stdout + completed.stderr
    matches = result_pattern.findall(combined)
    k_result = matches[0] if len(matches) == 1 else f"PARSE_ERROR:{matches}"
    python_result = canonical(first, second)
    print(
        f"KCASE {label}: first={first} second={second} "
        f"python={python_result} k={k_result} exit={completed.returncode}"
    )
    if completed.returncode != 0 or k_result != python_result:
        mismatches.append((label, first, second, python_result, k_result, combined))

print(f"K_CASES={len(cases)}")
print(f"K_MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches:
        print(f"K_MISMATCH={mismatch[:5]}")
        print(mismatch[5])
    raise SystemExit(1)
