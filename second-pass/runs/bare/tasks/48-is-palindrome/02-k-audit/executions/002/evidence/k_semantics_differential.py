#!/usr/bin/env python3
"""Execute the freshly built generated semantics and compare with both Python functions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys


WORK = Path("/tmp/audit-work/source")
DEFINITION = WORK / "semantic-kompiled-llvm"
PROGRAM = WORK / "solution.mpy"


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_palindrome


canonical = load_function(Path("/reference/canonical.py"), "canonical_for_k")
candidate = load_function(WORK / "solution.py", "candidate_for_k")

cases = [
    "",
    "a",
    "aa",
    "ab",
    "aba",
    "aaaaa",
    "zbcd",
    "abba",
    "abca",
    "a b a",
    "\x00",
    "\x00a\x00",
    "\n\t\n",
    "été",
    "éte",
    "e\u0301x\u0301e",
    "\u00ff",
    "\u0100",
    "\u4e2d",
    "🙂",
    "🙂🙃🙂",
    "🙂🙃",
    "𐀀x𐀀",
]

result_pattern = re.compile(r"PyBool\s*\(\s*(true|false)\s*\)")
records = []
failures = []
for text in cases:
    k_literal = json.dumps(text, ensure_ascii=False)
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        "-cFUNCTION=\"is_palindrome\"",
        f"-cARG={k_literal}",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    matches = result_pattern.findall(completed.stdout)
    k_value = matches[-1] == "true" if matches else None
    canonical_value = canonical(text)
    candidate_value = candidate(text)
    okay = (
        completed.returncode == 0
        and k_value is not None
        and type(canonical_value) is bool
        and type(candidate_value) is bool
        and k_value == canonical_value == candidate_value
    )
    record = {
        "input": text,
        "k_literal": k_literal,
        "command": command,
        "exit_status": completed.returncode,
        "k_result": k_value,
        "canonical_result": canonical_value,
        "candidate_python_result": candidate_value,
        "match": okay,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    records.append(record)
    if not okay:
        failures.append(record)

summary = {
    "program": str(PROGRAM),
    "definition": str(DEFINITION),
    "oracle": "/reference/canonical.py:is_palindrome",
    "candidate_python": str(WORK / "solution.py") + ":is_palindrome",
    "case_count": len(cases),
    "failure_count": len(failures),
    "records": records,
}
print(json.dumps(summary, ensure_ascii=True, indent=2))
sys.exit(1 if failures else 0)
