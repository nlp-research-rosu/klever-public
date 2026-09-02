#!/usr/bin/env python3
"""Ground witness for the generated-semantics/CPython recursion mismatch."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pstring(value: str) -> str:
    result = "eps"
    for char in reversed(value):
        result = f"ch({ord(char)}, {result})"
    return result


value = "abc" * 400
input_term = pstring(value)
program = "/tmp/audit-work/fresh/solution.mpy"
definition = "/tmp/audit-work/fresh/semantic-audit-kompiled"
command = ["krun", program, f"-cINPUT={input_term}", "--definition", definition]
completed = subprocess.run(command, text=True, capture_output=True)
combined = completed.stdout + completed.stderr
match = re.search(r"pyBool\s*\(\s*(true|false)\s*\)", combined)
k_result = None if match is None else match.group(1) == "true"

canonical = load_module("trusted_canonical_long", Path("/reference/canonical.py"))
candidate = load_module("candidate_solution_long", Path("/tmp/audit-work/fresh/solution.py"))
canonical_result = canonical.is_happy(value)
try:
    candidate_result: object = candidate.is_happy(value)
except Exception as exc:
    candidate_result = f"{type(exc).__name__}: {exc}"

print(f"input_expression='abc' * 400")
print(f"input_length={len(value)}")
print(f"input_sha256_utf8={hashlib.sha256(value.encode()).hexdigest()}")
print(f"k_input_term_length={len(input_term)}")
print(
    f"command_prefix={command[:2]!r} input_supplied_as=-cINPUT=<generated "
    f"{len(input_term)}-character exact PString term> "
    f"command_suffix={command[-2:]!r}"
)
print(f"krun_exit={completed.returncode}")
print(f"k_result={k_result!r}")
print(f"canonical_result={canonical_result!r}")
print(f"candidate_result={candidate_result!r}")
print("K_OUTPUT_BEGIN")
print(combined.rstrip())
print("K_OUTPUT_END")

expected_witness = (
    completed.returncode == 0
    and k_result is True
    and canonical_result is True
    and isinstance(candidate_result, str)
    and candidate_result.startswith("RecursionError:")
)
print(f"expected_mismatch_observed={expected_witness}")
raise SystemExit(0 if expected_witness else 1)
