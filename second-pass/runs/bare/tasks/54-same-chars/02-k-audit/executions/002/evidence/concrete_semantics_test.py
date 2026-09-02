#!/usr/bin/env python3
"""Compare fresh LLVM execution of generated semantic.k with both Python functions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scratch = Path("/tmp/audit-work/54-same-chars")
candidate_dir = scratch / "candidate"
canonical = load_module("concrete_canonical", scratch / "reference/canonical.py")
candidate = load_module("concrete_candidate", candidate_dir / "solution.py")

cases = [
    ("documented-true", "eabcdzzzz", "dddzzzzzzzddeddabc"),
    ("documented-false", "eabcd", "dddddddabc"),
    ("empty-empty", "", ""),
    ("empty-nonempty", "", "a"),
    ("duplicates", "aa", "a"),
    ("order", "ab", "ba"),
    ("left-extra", "abc", "ab"),
    ("nul", "\0", "\0\0"),
    ("unicode-bmp", "é", "éé"),
    ("unicode-distinct-normalization", "é", "e\u0301"),
    ("unicode-astral", "😀a", "a😀😀"),
    ("newline", "\n", "\n\n"),
]

mismatches = 0
for label, left, right in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cS0={json.dumps(left, ensure_ascii=False)}",
        f"-cS1={json.dumps(right, ensure_ascii=False)}",
    ]
    print("COMMAND:", shlex.join(command))
    result = subprocess.run(
        command,
        cwd=candidate_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    bounded_output = (result.stdout + result.stderr)[-4000:]
    match = re.search(
        r"result\s*\(\s*boolValue\s*\(\s*(true|false)\s*\)\s*\)",
        bounded_output,
    )
    k_value = None if match is None else match.group(1) == "true"
    canonical_value = canonical.same_chars(left, right)
    candidate_value = candidate.same_chars(left, right)
    agreed = (
        result.returncode == 0
        and k_value is not None
        and k_value == canonical_value == candidate_value
    )
    mismatches += not agreed
    print(
        f"CASE {label} left={left!r} right={right!r} "
        f"exit={result.returncode} k={k_value} "
        f"canonical={canonical_value} candidate={candidate_value} "
        f"agreed={agreed}"
    )
    if not agreed:
        print("BOUNDED_OUTPUT_START")
        print(bounded_output)
        print("BOUNDED_OUTPUT_END")

print(f"cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
