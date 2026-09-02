#!/usr/bin/env python3
"""Compare fresh `krun` execution with candidate Python and math.gcd."""

from __future__ import annotations

import importlib.util
import math
import re
import subprocess
from pathlib import Path

work = Path("/tmp/audit-work/reconstruction")
spec = importlib.util.spec_from_file_location("audit_solution", work / "solution.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import scratch solution.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
python_gcd = module.greatest_common_divisor

cases = [
    (3, 5),
    (25, 15),
    (0, 0),
    (0, 7),
    (7, 0),
    (-1, 0),
    (0, -1),
    (-25, 15),
    (25, -15),
    (-25, -15),
    (17, 17),
    (144, 12),
    (2**31 - 1, 2**16 - 1),
]

mismatches: list[tuple[int, int, int, int, int]] = []
for a, b in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "semantic-llvm-audit",
        f"-cA={a}",
        f"-cB={b}",
    ]
    completed = subprocess.run(
        command,
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print("COMMAND:", " ".join(command))
    print(f"EXIT_STATUS: {completed.returncode}")
    print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit(f"krun failed for {(a, b)}")
    match = re.search(r"<result>\s*result \( (-?[0-9]+) \)\s*</result>", completed.stdout)
    if match is None:
        raise SystemExit(f"no result cell parsed for {(a, b)}")
    k_result = int(match.group(1))
    python_result = python_gcd(a, b)
    contract_result = math.gcd(a, b)
    print(
        f"COMPARISON input=({a},{b}) k={k_result} "
        f"python={python_result} math.gcd={contract_result}"
    )
    if not (k_result == python_result == contract_result):
        mismatches.append((a, b, k_result, python_result, contract_result))

print(f"case_count={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(f"mismatches={mismatches}")
    raise SystemExit("generated semantics diverges from Python or math.gcd")
