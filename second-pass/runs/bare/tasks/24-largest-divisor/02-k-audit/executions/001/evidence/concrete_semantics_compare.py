#!/usr/bin/env python3
"""Compare fresh LLVM semantics execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/24-largest-divisor")
DEFINITION = WORK / "audit-semantic-kompiled"
INPUTS = [2, 3, 4, 15, 49, 101, 1024]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_divisor


def main() -> int:
    candidate = load(WORK / "solution.py", "candidate_concrete")
    canonical = load(WORK / "trusted-canonical.py", "canonical_concrete")
    failures = []
    records = []
    for value in INPUTS:
        command = [
            "krun",
            "solution.mpy",
            f"-cARG={value}",
            "--definition",
            str(DEFINITION),
            "--output",
            "pretty",
        ]
        process = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
        matches = re.findall(
            r"<result>\s*(-?[0-9]+)\s*</result>",
            process.stdout,
            flags=re.MULTILINE,
        )
        k_result = int(matches[-1]) if matches else None
        candidate_result = candidate(value)
        canonical_result = canonical(value)
        ok = (
            process.returncode == 0
            and k_result == candidate_result
            and k_result == canonical_result
            and "<k>\n    .K\n  </k>" in process.stdout
        )
        record = {
            "input": value,
            "command": command,
            "krun_exit": process.returncode,
            "k_result": k_result,
            "candidate_python_result": candidate_result,
            "canonical_python_result": canonical_result,
            "final_k_empty": "<k>\n    .K\n  </k>" in process.stdout,
            "match": ok,
            "krun_output": process.stdout,
        }
        records.append(record)
        if not ok:
            failures.append(record)
    print(json.dumps({"records": records, "failure_count": len(failures)}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
