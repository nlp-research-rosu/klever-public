#!/usr/bin/env python3
"""Execute the freshly built generated semantics and compare with Python."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/130-tri-audit")
DEFINITION = SCRATCH / "semantic-concrete-kompiled"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_oracle(n: int) -> list[int]:
    values = [1]
    for i in range(1, n + 1):
        if i == 1:
            values.append(3)
        elif i % 2 == 0:
            values.append(1 + i // 2)
        else:
            values.append(values[i - 1] + values[i - 2] + (i + 3) // 2)
    return values


def run_k(n: int) -> tuple[int, str, str]:
    command = [
        "krun",
        "solution.mpy",
        f"-cN={n}",
        "--definition",
        str(DEFINITION),
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    print(f"EXIT_STATUS={completed.returncode}")
    if completed.stderr:
        print(f"STDERR={completed.stderr.rstrip()}")
    output = completed.stdout
    print(f"STDOUT_BYTES={len(output.encode())}")
    print(f"STDOUT_SHA256={hashlib.sha256(output.encode()).hexdigest()}")
    print(f"STDOUT_PREFIX={output[:180]!r}")
    print(f"STDOUT_SUFFIX={output[-180:]!r}")
    return completed.returncode, output, completed.stderr


def parse_k_list(output: str) -> list[int]:
    assert "returned" in output and "LVal" in output, output
    return [
        int(value)
        for value in re.findall(r"\bcons\s*\(\s*(-?[0-9]+)\s*,", output)
    ]


candidate = load_module("candidate_for_k_compare", SCRATCH / "solution.py")
canonical = load_module("canonical_for_k_compare", SCRATCH / "canonical.py")

normal_inputs = [0, 1, 2, 3, 4, 5, 6, 10, 25, 50]
for n in normal_inputs:
    returncode, output, _ = run_k(n)
    assert returncode == 0
    k_values = parse_k_list(output)
    candidate_values = candidate.tri(n)
    canonical_values = canonical.tri(n)
    oracle_values = contract_oracle(n)
    assert k_values == candidate_values
    assert k_values == canonical_values
    assert k_values == oracle_values
    print(
        f"N={n} K_LENGTH={len(k_values)} K_LAST={k_values[-1]} "
        "PYTHON_NUMERIC_MATCH=True"
    )

large_n = 1100
returncode, output, _ = run_k(large_n)
assert returncode == 0
k_values = parse_k_list(output)
oracle_values = contract_oracle(large_n)
assert k_values == oracle_values
try:
    candidate.tri(large_n)
except Exception as error:
    candidate_status = f"raise:{type(error).__name__}:{error}"
else:
    candidate_status = "return"
canonical_values = canonical.tri(large_n)
assert canonical_values == oracle_values
print(
    f"N={large_n} K_STATUS=return K_LENGTH={len(k_values)} "
    f"K_LAST={k_values[-1]} CANDIDATE_PYTHON_STATUS={candidate_status} "
    "CANONICAL_PYTHON_STATUS=return"
)
assert candidate_status.startswith("raise:RecursionError:")
print("CONCRETE_SEMANTICS_COMPARE_PASS")
