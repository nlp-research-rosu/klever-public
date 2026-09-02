#!/usr/bin/env python3
"""Compare fresh concrete K execution with independent Python behavior."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
DEFINITION = WORK / "semantic-audit-kompiled"


def load_candidate():
    spec = importlib.util.spec_from_file_location("candidate_for_k_diff", WORK / "solution.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


candidate = load_candidate()


def contract_oracle(text: str) -> int:
    value = Decimal(text)
    if not value.is_finite():
        raise ValueError("finite values only")
    numerator, denominator = value.as_integer_ratio()
    magnitude, remainder = divmod(abs(numerator), denominator)
    rounded = magnitude + int(2 * remainder >= denominator)
    return rounded if numerator >= 0 else -rounded


cases = [
    "10",
    "15.3",
    "14.5",
    "-14.5",
    "0",
    "-0",
    "0.49",
    "0.5",
    "0.51",
    "-0.49",
    "-0.5",
    "-0.51",
    ".5",
    "-.5",
    "+2.5",
    "1e2",
    "2.5e0",
    "-2.5E+0",
    "1.50e2",
    "1.499999999999999999999999",
    "1.500000000000000000000001",
    "9007199254740992.5",
    "-9007199254740992.5",
    " 2.5 ",
    "1_000.5",
]

failures = 0
for text in cases:
    argument = f"pyStr({json.dumps(text)})"
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARG={argument}",
    ]
    run = subprocess.run(command, cwd=WORK, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    match = re.search(r"<result>\s*pyInt\s*\(\s*(-?\d+)\s*\)\s*</result>", run.stdout)
    k_result = int(match.group(1)) if match else None
    try:
        python_result = candidate(text)
        oracle_result = contract_oracle(text)
        python_outcome = ("value", python_result)
        oracle_outcome = ("value", oracle_result)
    except Exception as error:
        python_outcome = ("exception", type(error).__name__, str(error))
        oracle_outcome = python_outcome
    ok = run.returncode == 0 and k_result == python_result == oracle_result
    if not ok:
        failures += 1
    compact_output = " ".join(run.stdout.split())
    print(
        f"input={text!r} command={command!r} exit={run.returncode} "
        f"k_result={k_result!r} python={python_outcome!r} oracle={oracle_outcome!r} "
        f"status={'OK' if ok else 'MISMATCH'}"
    )
    if not ok:
        print(f"K_OUTPUT {compact_output[:1200]}")

print(f"cases={len(cases)} mismatches={failures}")
raise SystemExit(1 if failures else 0)
