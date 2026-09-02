#!/usr/bin/env python3
"""Concrete satisfiability and postcondition-substitution witnesses."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


def length_result(length: int) -> str:
    if length < 2:
        return "NO"
    divisor = 2
    while divisor * divisor <= length:
        if length % divisor == 0:
            return "NO"
        divisor += 1
    return "YES"


ROOT = Path("/tmp/audit-work/127-intersection")
RUN = ROOT / "run"
canonical = load_entry(ROOT / "trusted" / "canonical.py", "canonical_for_witness")
candidate = load_entry(RUN / "solution.py", "candidate_for_witness")

# (A,B,C,D), expected entry case, and the exact RHS arithmetic for that case.
witnesses = [
    ((0, 4, -1, 5), 1, lambda a, b, c, d: b - a),
    ((0, 10, -2, 1), 2, lambda a, b, c, d: d - a),
    ((0, 4, 2, 6), 3, lambda a, b, c, d: b - c),
    ((0, 10, 2, 7), 4, lambda a, b, c, d: d - c),
]

result_pattern = re.compile(r'strVal\s*\(\s*"(YES|NO)"\s*\)')
failures = []

for endpoints, expected_case, rhs in witnesses:
    a, b, c, d = endpoints
    cases = [
        a <= b and c <= d and c <= a and d >= b,
        a <= b and c <= d and c <= a and d < b,
        a <= b and c <= d and c > a and d >= b,
        a <= b and c <= d and c > a and d < b,
    ]
    active_cases = [index + 1 for index, active in enumerate(cases) if active]
    claimed_length = rhs(a, b, c, d)
    claimed_value = length_result(claimed_length)
    first = (a, b)
    second = (c, d)
    canonical_value = canonical(first, second)
    candidate_value = candidate(first, second)

    command = [
        "krun",
        str(RUN / "solution.mpy"),
        "--definition",
        str(RUN / "semantic-fresh-kompiled"),
        f"-cINTERVAL1=TupleExpr(Int({a}),Int({b}))",
        f"-cINTERVAL2=TupleExpr(Int({c}),Int({d}))",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(command, cwd=RUN, text=True, capture_output=True)
    k_matches = result_pattern.findall(completed.stdout + completed.stderr)
    k_value = k_matches[0] if len(k_matches) == 1 else f"PARSE_ERROR:{k_matches}"

    print(
        f"ENTRY_WITNESS expected_case={expected_case} active_cases={active_cases} "
        f"A={a} B={b} C={c} D={d} claimed_length={claimed_length} "
        f"claimed_value={claimed_value} canonical={canonical_value} "
        f"candidate={candidate_value} k={k_value} k_exit={completed.returncode}"
    )
    if (
        active_cases != [expected_case]
        or claimed_value != canonical_value
        or claimed_value != candidate_value
        or claimed_value != k_value
        or completed.returncode != 0
    ):
        failures.append(endpoints)

print(f"ENTRY_WITNESSES={len(witnesses)}")
print(f"ENTRY_WITNESS_FAILURES={len(failures)}")
if failures:
    raise SystemExit(1)
