#!/usr/bin/env python3
"""Compare fresh LLVM semantics execution with independent Python execution."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any, Callable


ROOT = Path("/tmp/audit-work/fresh")
SOLUTION = ROOT / "candidate" / "solution.py"
PROGRAM = ROOT / "candidate" / "solution.mpy"
DEFINITION = ROOT / "candidate" / "concrete-kompiled"
INPUTS = Path("/audit-output/evidence/k_concrete_inputs.json")
TOKEN_RE = re.compile(
    r'\.List|-?[0-9]+|[A-Za-z_][A-Za-z_0-9]*|"(?:\\.|[^"\\])*"|[()]'
)


def load_entry(path: Path) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location("candidate_python", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "split_words")


def k_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def encode_value(value: Any) -> str:
    if type(value) is int:
        return f"VInt({value})"
    if type(value) is list and all(type(item) is str for item in value):
        items = " ".join(f"ListItem(VStr({k_string(item)}))" for item in value)
        return f"VList({items if items else '.List'})"
    raise TypeError(f"unsupported Python result: {value!r}")


def normalize(term: str) -> tuple[str, ...]:
    return tuple(TOKEN_RE.findall(term))


def extract_k_result(output: str) -> str:
    match = re.search(r"<k>\s*(.*?)\s*~>\s*\.K\s*</k>", output, re.DOTALL)
    if match is None:
        raise ValueError(f"unexpected krun output: {output!r}")
    return match.group(1)


def main() -> int:
    python_entry = load_entry(SOLUTION)
    inputs = json.loads(INPUTS.read_text(encoding="utf-8"))
    mismatches = 0
    command_failures = 0
    print("PYTHON_ORACLE:", SOLUTION)
    print("K_PROGRAM:", PROGRAM)
    print("FRESH_DEFINITION:", DEFINITION)
    print("INPUT_FILE:", INPUTS)
    print("CASE_COUNT:", len(inputs))
    for index, value in enumerate(inputs):
        input_term = k_string(value)
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={input_term}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        expected = encode_value(python_entry(value))
        actual = ""
        equal = False
        parse_error = None
        if completed.returncode == 0:
            try:
                actual = extract_k_result(completed.stdout)
                equal = normalize(actual) == normalize(expected)
            except ValueError as err:
                parse_error = str(err)
        if completed.returncode != 0:
            command_failures += 1
        if not equal:
            mismatches += 1
        print(
            json.dumps(
                {
                    "case": index,
                    "input": value,
                    "command": shlex.join(command),
                    "exit_status": completed.returncode,
                    "python_result": python_entry(value),
                    "expected_k": expected,
                    "actual_k": actual,
                    "equal": equal,
                    "parse_error": parse_error,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print("COMMAND_FAILURES:", command_failures)
    print("MISMATCH_COUNT:", mismatches)
    return 0 if command_failures == 0 and mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
