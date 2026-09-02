#!/usr/bin/env python3
"""Compare fresh krun results with independent Python execution."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
EVIDENCE = Path("/audit-output/evidence")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


solution = load(ROOT / "solution.py", "solution_for_krun_comparison")
canonical = load(ROOT / "canonical.py", "canonical_for_krun_comparison")
cases = {
    "3-4-5": (3, 4, 5),
    "1-2-3": (1, 2, 3),
    "5-3-4": (5, 3, 4),
    "3-5-4": (3, 5, 4),
    "0-0-0": (0, 0, 0),
    "0-3-3": (0, 3, 3),
    "3-0-3": (3, 0, 3),
    "3-3-0": (3, 3, 0),
    "neg3-4-5": (-3, 4, 5),
    "3-neg4-5": (3, -4, 5),
    "3-4-neg5": (3, 4, -5),
    "large": (300000000000000000000, 400000000000000000000, 500000000000000000000),
}

mismatches = 0
for name, values in cases.items():
    text = (EVIDENCE / f"09c-krun-{name}.log").read_text()
    match = re.search(r"result \( (true|false) \)", text)
    if match is None:
        raise SystemExit(f"no K result in {name}")
    k_result = match.group(1) == "true"
    python_result = solution(*values)
    canonical_result = canonical(*values)
    agree = k_result == python_result
    mismatches += not agree
    print(
        f"{name}: args={values} K={k_result} "
        f"solution.py={python_result} canonical.py={canonical_result} "
        f"K_solution_agree={agree}"
    )

print(f"K_solution_mismatches={mismatches}")
if mismatches:
    raise SystemExit(1)
