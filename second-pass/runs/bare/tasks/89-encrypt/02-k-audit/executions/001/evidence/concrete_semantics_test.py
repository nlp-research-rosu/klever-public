#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with submitted Python."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


def load_encrypt(path: Path):
    spec = importlib.util.spec_from_file_location("generated_solution_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


solution = load_encrypt(Path("/tmp/audit-work/source/solution.py"))
program = "/tmp/audit-work/source/solution.mpy"
definition = "/tmp/audit-work/build/concrete-kompiled"
cases = [
    "",
    "a",
    "v",
    "w",
    "x",
    "y",
    "z",
    "hi",
    "asdfghjkl",
    "xyz",
    "A",
    "0",
    " ",
    "a-z",
    "hello world",
    "é",
    "🙂",
]
result_pattern = re.compile(r"<result>\s*(\"(?:\\.|[^\"\\])*\")\s*</result>", re.S)
records = []

for value in cases:
    command = [
        "krun",
        program,
        "-cINPUT=" + json.dumps(value, ensure_ascii=False),
        "--definition",
        definition,
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    match = result_pattern.search(completed.stdout)
    if completed.returncode == 0 and match:
        k_outcome = {"kind": "return", "value": json.loads(match.group(1))}
    else:
        k_outcome = {
            "kind": "tool_failure",
            "exit": completed.returncode,
            "stdout": completed.stdout[-2000:],
            "stderr": completed.stderr[-2000:],
        }
    try:
        py_outcome = {"kind": "return", "value": solution(value)}
    except Exception as exc:
        py_outcome = {
            "kind": "exception",
            "type": type(exc).__name__,
            "message": str(exc),
        }
    record = {
        "input": value,
        "command": command,
        "krun": k_outcome,
        "python": py_outcome,
        "match": k_outcome == py_outcome,
    }
    records.append(record)
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))

Path("/audit-output/evidence/concrete-semantics-results.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
mismatches = sum(not record["match"] for record in records)
print(f"cases={len(records)} mismatches={mismatches}")
raise SystemExit(0 if mismatches == 0 else 1)
