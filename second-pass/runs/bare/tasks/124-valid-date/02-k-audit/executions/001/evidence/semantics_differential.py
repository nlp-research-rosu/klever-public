#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with the real Python program."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any, Callable


EVIDENCE_DIR = Path("/audit-output/evidence")
PROGRAM_PATH = Path("/audit-output/evidence/regenerated-solution.mpy")
DEFINITION = "/tmp/audit-work/semantic-audit-kompiled"

CASES = [
    ("normal_valid", "03-11-2000"),
    ("empty", ""),
    ("length_9", "03-11-200"),
    ("length_11", "03-11-20000"),
    ("separator", "06/04/2020"),
    ("month_nondigit", "a3-11-2000"),
    ("month_00", "00-01-2020"),
    ("month_13", "13-01-2020"),
    ("feb_01", "02-01-2020"),
    ("feb_29", "02-29-1900"),
    ("feb_30", "02-30-2020"),
    ("thirty_30", "04-30-2020"),
    ("thirty_31", "04-31-2020"),
    ("thirtyone_31", "01-31-0000"),
    ("thirtyone_32", "01-32-9999"),
    ("arabic_indic", "٠٣-١١-٢٠٠٠"),
    ("superscript_digit", "⁰3-11-2000"),
]


def load_generated() -> Callable[[str], bool]:
    path = "/tmp/audit-work/candidate-src/solution.py"
    spec = importlib.util.spec_from_file_location("generated_for_semantics", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def python_result(entry: Callable[[str], bool], value: str) -> Any:
    try:
        return {"kind": "value", "value": entry(value)}
    except Exception as exc:
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}


def main() -> int:
    entry = load_generated()
    program = " ".join(PROGRAM_PATH.read_text(encoding="utf-8").splitlines())
    rows: list[dict[str, Any]] = []
    mismatch_count = 0
    for label, value in CASES:
        command_term = (
            f"runProgram({program}, "
            f'"valid_date", vals(strVal({json.dumps(value, ensure_ascii=False)})))'
        )
        command = [
            "krun",
            "--definition",
            DEFINITION,
            f"-cPGM={command_term}",
            "--output",
            "program",
        ]
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        match = re.search(r"boolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
        if completed.returncode == 0 and match:
            k_result: Any = {"kind": "value", "value": match.group(1) == "true"}
        else:
            k_result = {
                "kind": "execution_failure",
                "exit_status": completed.returncode,
                "parsed_boolean": bool(match),
            }
        py_result = python_result(entry, value)
        same = k_result == py_result
        if not same:
            mismatch_count += 1
        rows.append(
            {
                "label": label,
                "input": value,
                "command": shlex.join(command),
                "exit_status": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "k_result": k_result,
                "python_result": py_result,
                "same": same,
            }
        )

    result = {
        "definition": DEFINITION,
        "program": str(PROGRAM_PATH),
        "case_count": len(rows),
        "mismatch_count": mismatch_count,
        "cases": rows,
    }
    (EVIDENCE_DIR / "semantics_differential_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"case_count={len(rows)} mismatch_count={mismatch_count}")
    for row in rows:
        print(
            json.dumps(
                {
                    "label": row["label"],
                    "input": row["input"],
                    "exit_status": row["exit_status"],
                    "k_result": row["k_result"],
                    "python_result": row["python_result"],
                    "same": row["same"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
