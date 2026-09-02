#!/usr/bin/env python3
"""Compare fresh LLVM-semantics results with independent Python execution."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


log_path = Path("/audit-output/evidence/stage3/krun-boundaries.log")
text = log_path.read_text()
case_pattern = re.compile(
    r"CASE n=(-?\d+) x=(-?\d+) y=(-?\d+)\n"
    r"(.*?)(?=\nCASE n=|\nEXIT_STATUS:)",
    re.DOTALL,
)
result_pattern = re.compile(
    r"<result>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K\s*</result>",
    re.DOTALL,
)

spec = importlib.util.spec_from_file_location(
    "generated_solution_for_krun_check",
    "/tmp/audit-work/rebuild/solution.py",
)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import generated solution")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

seen = 0
for match in case_pattern.finditer(text):
    n, x, y = map(int, match.group(1, 2, 3))
    result_match = result_pattern.search(match.group(4))
    if result_match is None:
        raise AssertionError(f"no final result parsed for n={n}, x={x}, y={y}")
    k_result = int(result_match.group(1))
    python_result = module.x_or_y(n, x, y)
    print(
        f"n={n},x={x},y={y},"
        f"k_result={k_result},python_result={python_result},"
        f"match={k_result == python_result}"
    )
    assert k_result == python_result
    seen += 1

print(f"checked_case_count={seen}")
assert seen == 11
