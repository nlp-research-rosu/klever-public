#!/usr/bin/env python3
"""Compare the idealized K execution with CPython at the recursion boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
from pathlib import Path


LENGTH = 998
WORK = Path("/tmp/audit-work/audit-62")


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


xs = list(range(LENGTH))
args_term = "ListV(" + ", ".join(f"IntV({value})" for value in xs) + ")"
command = [
    "krun",
    "solution.mpy",
    "--definition",
    "semantic-audit-kompiled",
    "-cARGS=" + args_term,
]

print(f"input_length={LENGTH} input_head={xs[:5]} input_tail={xs[-5:]}")
print(f"args_term_sha256={hashlib.sha256(args_term.encode()).hexdigest()}")
print("inner_command_schema=krun solution.mpy --definition semantic-audit-kompiled -cARGS=<args_term>")
completed = subprocess.run(
    command,
    cwd=WORK,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
print(f"inner_exit_status={completed.returncode}")
print(f"inner_output_sha256={hashlib.sha256(completed.stdout.encode()).hexdigest()}")
print(f"inner_output_bytes={len(completed.stdout.encode())}")

k_values = [
    int(match)
    for match in re.findall(r"IntV\s*\(\s*(-?[0-9]+)\s*\)", completed.stdout)
]
expected_values = [index * xs[index] for index in range(1, LENGTH)]
normal_final = "~> .K" in completed.stdout and len(k_values) == LENGTH - 1
print(
    f"k_normal_final={normal_final} k_value_count={len(k_values)} "
    f"k_head={k_values[:5]} k_tail={k_values[-5:]} "
    f"k_matches_derivative={k_values == expected_values}"
)

canonical = load("canonical_long", "/reference/canonical.py")
generated = load("generated_long", str(WORK / "solution.py"))
canonical_result = canonical.derivative(list(xs))
print(
    f"canonical_kind=return canonical_length={len(canonical_result)} "
    f"canonical_matches_expected={canonical_result == expected_values}"
)
try:
    generated.derivative(list(xs))
except Exception as error:
    print(f"generated_kind=exception generated_exception={type(error).__name__}")
    generated_raised_recursion = isinstance(error, RecursionError)
else:
    print("generated_kind=return")
    generated_raised_recursion = False

if not (
    completed.returncode == 0
    and normal_final
    and k_values == expected_values
    and canonical_result == expected_values
    and generated_raised_recursion
):
    raise SystemExit(1)
