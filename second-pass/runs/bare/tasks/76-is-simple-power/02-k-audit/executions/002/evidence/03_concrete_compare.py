#!/usr/bin/env python3
"""Run the freshly rebuilt generated semantics and compare it with Python."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/76-is-simple-power")
DEFINITION = ROOT / "fresh-semantic-kompiled"
PROGRAM = ROOT / "solution.mpy"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generated = load(ROOT / "solution.py", "generated_solution")
canonical = load(Path("/reference/canonical.py"), "trusted_canonical_for_concrete")

# Together these exercise both branches of every If, the x==1 and x<1
# boundaries, n<2 and n==2, zero/one/multiple While iterations, exact hits,
# overshoots, assignment/multiplication, and both Boolean return literals.
cases = [
    (-1, 2),
    (0, 2),
    (1, 4),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, 2),
    (8, 2),
    (5, 3),
    (4, -2),
    (16, 4),
    (15, 4),
]

mismatches_with_generated = 0
mismatches_with_canonical = 0

for x, n in cases:
    command = [
        "krun",
        str(PROGRAM),
        f"-cX={x}",
        f"-cN={n}",
        "--definition",
        str(DEFINITION),
    ]
    completed = subprocess.run(command, check=False, text=True, capture_output=True)
    print("$ " + shlex.join(command))
    print(f"EXIT={completed.returncode}")
    if completed.stderr:
        print("STDERR:")
        print(completed.stderr.rstrip())
    print("STDOUT:")
    print(completed.stdout.rstrip())

    match = re.search(r"<result>\s*(true|false)\s*</result>", completed.stdout)
    k_result = None if match is None else match.group(1) == "true"
    python_result = generated.is_simple_power(x, n)
    canonical_result = canonical.is_simple_power(x, n)
    matches_generated = completed.returncode == 0 and k_result == python_result
    matches_canonical = completed.returncode == 0 and k_result == canonical_result
    mismatches_with_generated += not matches_generated
    mismatches_with_canonical += not matches_canonical
    print(
        "SUMMARY "
        f"x={x} n={n} K={k_result!r} generated_python={python_result!r} "
        f"canonical_python={canonical_result!r} "
        f"K_matches_generated={matches_generated} K_matches_canonical={matches_canonical}"
    )

print(f"TOTAL_CASES={len(cases)}")
print(f"K_VS_GENERATED_MISMATCHES={mismatches_with_generated}")
print(f"K_VS_CANONICAL_MISMATCHES={mismatches_with_canonical}")
raise SystemExit(0 if mismatches_with_generated == 0 else 1)
