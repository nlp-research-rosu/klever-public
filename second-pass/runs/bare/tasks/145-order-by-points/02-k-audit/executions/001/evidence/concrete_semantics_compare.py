#!/usr/bin/env python3
"""Compare fresh LLVM-semantics runs with both independent Python functions."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/proof145")
DEFINITION = WORK / "semantic-audit-kompiled"
RESULTS = Path("/audit-output/evidence/concrete-semantics-results.json")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order_by_points


def input_term(values):
    return "ListExpr(" + ", ".join(f"Int({value})" for value in values) + ")"


def expected_output_term(values):
    if not values:
        return "ListVal(.Vals)"
    return "ListVal(" + ",".join(f"IntVal({value})" for value in values) + ",.Vals)"


canonical = load(Path("/reference/canonical.py"), "concrete_trusted_canonical")
candidate = load(WORK / "solution.py", "concrete_fresh_candidate")

cases = [
    ("documented", [1, 11, -1, -11, -12]),
    ("empty", []),
    ("zero-sign-decimal-boundary", [0, 100, -100, 10, -10, 1, -1]),
    ("tie-stability", [12, 21, -12, 3]),
    (
        "arbitrary-precision",
        [12345678901234567890, -12345678901234567890, 10**60, -(10**60)],
    ),
]

records = []
failed = False
for label, values in cases:
    expected = canonical(list(values))
    candidate_result = candidate(list(values))
    command = [
        "krun",
        "solution.mpy",
        f"-cINPUT={input_term(values)}",
        "--definition",
        str(DEFINITION),
    ]
    print(f"CASE: {label}")
    print("COMMAND:", json.dumps(command))
    completed = subprocess.run(command, cwd=WORK, text=True, capture_output=True)
    print("KRUN_STDOUT_BEGIN")
    print(completed.stdout, end="")
    print("KRUN_STDOUT_END")
    if completed.stderr:
        print("KRUN_STDERR_BEGIN")
        print(completed.stderr, end="")
        print("KRUN_STDERR_END")
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    match = re.search(r"<output>\s*(.*?)\s*</output>", completed.stdout, re.S)
    actual_term = re.sub(r"\s+", "", match.group(1)) if match else None
    expected_term = expected_output_term(expected)
    ok = (
        completed.returncode == 0
        and expected == candidate_result
        and actual_term == expected_term
    )
    print(f"PYTHON_CANONICAL: {expected}")
    print(f"PYTHON_CANDIDATE: {candidate_result}")
    print(f"K_OUTPUT_NORMALIZED: {actual_term}")
    print(f"EXPECTED_K_OUTPUT: {expected_term}")
    print(f"MATCH: {ok}")
    records.append(
        {
            "label": label,
            "input": values,
            "command": command,
            "krun_exit_status": completed.returncode,
            "python_canonical": expected,
            "python_candidate": candidate_result,
            "k_output_normalized": actual_term,
            "expected_k_output": expected_term,
            "match": ok,
        }
    )
    failed |= not ok

RESULTS.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
print(f"TOTAL_CASES: {len(records)}")
print(f"MISMATCHES: {sum(not item['match'] for item in records)}")
raise SystemExit(1 if failed else 0)
