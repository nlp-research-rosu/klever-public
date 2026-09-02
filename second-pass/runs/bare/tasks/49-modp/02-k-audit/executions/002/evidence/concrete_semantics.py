#!/usr/bin/env python3
"""Run fresh LLVM semantics on normal/boundary inputs and compare Python."""

from __future__ import annotations

import importlib.util
import os
import re
import signal
import subprocess
import sys
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/fresh")
DEFINITION = ROOT / "semantic-llvm-kompiled"
MPY = ROOT / "solution.mpy"


def load_function(path: Path, name: str) -> Callable[[int, int], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


generated = load_function(ROOT / "solution.py", "semantics_generated")
canonical = load_function(ROOT / "trusted" / "canonical.py", "semantics_canonical")


def py_outcome(function: Callable[[int, int], int], n: int, p: int) -> tuple[str, object]:
    try:
        return ("value", function(n, p))
    except Exception as error:
        return ("exception", type(error).__name__)


def k_outcome(n: int, p: int) -> tuple[tuple[str, object], int, str]:
    command = [
        "krun",
        str(MPY),
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
        f"-cP={p}",
    ]
    print("COMMAND:", " ".join(command))
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=6)
        returncode = process.returncode
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate()
        normalized = output.replace("\x1b[0m", "")
        bounded = "\n".join(normalized.splitlines()[:30])
        return ("timeout", "6 seconds"), 124, bounded
    normalized = output.replace("\x1b[0m", "")
    match = re.search(r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", normalized)
    if returncode == 0 and match:
        result: tuple[str, object] = ("value", int(match.group(1)))
    elif returncode == 0:
        result = ("stuck-or-nonvalue", "no integer result")
    else:
        first_line = next((line for line in normalized.splitlines() if line.strip()), "")
        result = ("tool-error", first_line.strip())
    bounded = "\n".join(normalized.splitlines()[:30])
    return result, returncode, bounded


formal_cases = [
    (3, 5),
    (1101, 101),
    (0, 101),
    (0, 1),
    (1, 1),
    (1, 2),
    (2, 2),
    (40, 97),
]
outside_claim_cases = [(-1, 5), (0, 0), (2, -5), (0, -1)]

formal_failures = 0
for category, cases in (
    ("formal_claim_domain", formal_cases),
    ("outside_claim_boundary", outside_claim_cases),
):
    print(f"===== {category} =====")
    for n, p in cases:
        generated_result = py_outcome(generated, n, p)
        canonical_result = py_outcome(canonical, n, p)
        k_result, k_status, k_output = k_outcome(n, p)
        print(
            f"CASE n={n} p={p} generated={generated_result} "
            f"canonical={canonical_result} k={k_result} k_exit={k_status}"
        )
        print(k_output)
        if category == "formal_claim_domain" and k_result != generated_result:
            formal_failures += 1

print(f"formal_semantics_vs_generated_python_mismatches={formal_failures}")
print("CONCRETE_FORMAL_MATCH" if formal_failures == 0 else "CONCRETE_FORMAL_MISMATCH")
sys.exit(0 if formal_failures == 0 else 1)
