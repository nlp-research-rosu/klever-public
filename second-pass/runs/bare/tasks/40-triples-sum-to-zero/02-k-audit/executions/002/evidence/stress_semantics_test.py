#!/usr/bin/env python3
"""Exercise the generated semantics at the CPython recursion-gap witness."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "stress_oracle")
generated = load(
    Path("/tmp/audit-work/candidate-src/solution.py"), "stress_candidate"
)
values = [10**9, 1, -1, 0] + [2] * 997
ints = " ; ".join(map(str, values))
command = [
    "krun",
    "solution.mpy",
    "--definition",
    "/tmp/audit-work/semantics-kompiled",
    f"-cINPUT=VList({ints} ; .Ints)",
    "--output",
    "pretty",
]
completed = subprocess.run(
    command,
    cwd="/tmp/audit-work/candidate-src",
    capture_output=True,
    text=True,
    check=False,
)
matches = re.findall(
    r"result \( VBool \( (true|false) \) \)", completed.stdout
)
k_result = matches[0] == "true" if len(matches) == 1 else None
oracle_result = canonical(values)
try:
    generated_result = generated(values)
except Exception as error:
    generated_result = f"{type(error).__name__}: {error}"

print(f"stress_length={len(values)}")
print(f"canonical_result={oracle_result!r}")
print(f"generated_python_result={generated_result!r}")
print(f"k_exit_status={completed.returncode}")
print(f"k_result={k_result!r}")
print(f"k_matches_canonical={k_result is oracle_result}")
print(f"k_matches_generated_python={k_result == generated_result}")

valid_k_run = completed.returncode == 0 and k_result is oracle_result
raise SystemExit(0 if valid_k_run else 1)
