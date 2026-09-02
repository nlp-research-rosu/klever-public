#!/usr/bin/env python3
"""Compare fresh LLVM K execution with independent Python execution."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


candidate = load_entry(
    Path("/tmp/audit-work/source/solution.py"), "scratch_solution_for_k_compare"
)
canonical = load_entry(Path("/reference/canonical.py"), "canonical_for_k_compare")

cases = [
    "",
    "A",
    "7",
    " a",
    "aa",
    "apple pie",
    "apple pi e",
    "apple pi e ",
    "é",
    "x é",
    "α",
    "x α",
]

definition = "/tmp/audit-work/build/concrete-haskell-kompiled"
program = "/tmp/audit-work/source/solution.mpy"
k_result_pattern = re.compile(r"pyBool\s*\(\s*(true|false)\s*\)")
mismatches = []

for text in cases:
    command = [
        "krun",
        program,
        "--definition",
        definition,
        "-cTXT=" + json.dumps(text, ensure_ascii=False),
    ]
    try:
        completed = subprocess.run(
            command, text=True, capture_output=True, timeout=20
        )
    except subprocess.TimeoutExpired as error:
        print(f"INPUT={text!r}", flush=True)
        print(f"COMMAND={shlex.join(command)}", flush=True)
        print("KRUN_TIMEOUT_SECONDS=20", flush=True)
        mismatches.append((text, None, ("timeout",), 124))
        continue
    combined = completed.stdout + completed.stderr
    matches = k_result_pattern.findall(combined)
    k_result = None if not matches else matches[-1] == "true"
    try:
        python_result = ("return", candidate(text))
    except Exception as error:
        python_result = ("raise", type(error).__name__, str(error))
    try:
        canonical_result = ("return", canonical(text))
    except Exception as error:
        canonical_result = ("raise", type(error).__name__, str(error))

    print(f"INPUT={text!r}", flush=True)
    print(f"COMMAND={shlex.join(command)}", flush=True)
    print(f"KRUN_EXIT_STATUS={completed.returncode}", flush=True)
    print("KRUN_OUTPUT_BEGIN", flush=True)
    print(combined.rstrip(), flush=True)
    print("KRUN_OUTPUT_END", flush=True)
    print(f"K_PARSED_RESULT={k_result!r}", flush=True)
    print(f"PYTHON_CANDIDATE_RESULT={python_result!r}", flush=True)
    print(f"PYTHON_CANONICAL_RESULT={canonical_result!r}", flush=True)
    if completed.returncode != 0 or python_result != ("return", k_result):
        mismatches.append((text, k_result, python_result, completed.returncode))

print(f"case_count={len(cases)}")
print(f"k_vs_python_candidate_mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"K_VS_PYTHON_MISMATCH={mismatch!r}")

# Keep this evidence collector successful even when it exposes semantic defects.
