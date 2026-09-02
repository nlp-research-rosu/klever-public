#!/usr/bin/env python3
"""Witness the generated semantics omitting CPython recursion failure."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shlex
import subprocess
import sys


ROOT = Path("/tmp/audit-work/change-base-audit-20260726")
CANDIDATE = ROOT / "candidate"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load(ROOT / "reference/canonical.py", "krec_canonical")
submitted = load(CANDIDATE / "solution.py", "krec_submitted")

exponent = 997
x = 2**exponent
expected = canonical(x, 2)
try:
    submitted(x, 2)
    submitted_outcome = "returned"
except Exception as err:
    submitted_outcome = f"raised {type(err).__name__}: {err}"

command = [
    "krun",
    "solution.mpy",
    f"-cX={x}",
    "-cBASE=2",
    "--definition",
    "semantic-llvm-search-kompiled",
    "--pattern",
    f'<k> strVal("{expected}") ~> .K </k>',
]
process = subprocess.run(
    command,
    cwd=CANDIDATE,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

print(f"python_recursion_limit={sys.getrecursionlimit()}")
print(f"x=2**{exponent} x_bit_length={x.bit_length()}")
print(f"canonical_result_length={len(expected)}")
print(f"submitted_python_outcome={submitted_outcome}")
print(f"k_command={shlex.join(command)}")
print(f"k_exit={process.returncode}")
print(f"k_output={process.stdout.strip()!r}")

k_returns_expected = process.returncode == 0 and process.stdout.strip() == "#Top"
print(f"k_returns_canonical_string={k_returns_expected}")
sys.exit(0 if k_returns_expected and submitted_outcome.startswith("raised ") else 1)
