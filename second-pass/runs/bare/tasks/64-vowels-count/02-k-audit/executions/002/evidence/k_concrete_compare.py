#!/usr/bin/env python3
"""Run fresh generated K semantics and compare final values with Python."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
from typing import Callable


WORK = Path("/tmp/audit-work/64-vowels-count")
DEFINITION = WORK / "audit-semantic-kompiled"


def load_entry(path: Path, module_name: str) -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


generated = load_entry(WORK / "solution.py", "k_compare_generated")
cases = [
    "",
    "abcde",
    "ACEDY",
    "a",
    "b",
    "y",
    "Y",
    "ay",
    "ya",
    "by",
    "yb",
    "rhythm",
    "AEIOU",
    "bcdfg",
    "éy",
    "🙂Y",
]

failures: list[dict[str, object]] = []
for value in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={json.dumps(value, ensure_ascii=False)}",
        "--output",
        "pretty",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    result = subprocess.run(
        command,
        cwd=WORK,
        capture_output=True,
        text=True,
        check=False,
    )
    print(f"EXIT_STATUS: {result.returncode}")
    print("STDOUT_BEGIN")
    print(result.stdout.rstrip())
    print("STDOUT_END")
    if result.stderr:
        print("STDERR_BEGIN")
        print(result.stderr.rstrip())
        print("STDERR_END")
    match = re.search(r"<k>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K\s*</k>", result.stdout)
    observed = int(match.group(1)) if match else None
    expected = generated(value)
    print(
        f"COMPARISON input={value!r} python={expected} "
        f"k={observed} match={observed == expected}"
    )
    if result.returncode != 0 or observed != expected:
        failures.append(
            {
                "input": value,
                "status": result.returncode,
                "expected": expected,
                "observed": observed,
            }
        )

print(f"concrete_case_count={len(cases)}")
print(f"concrete_failure_count={len(failures)}")
print(f"concrete_failures={failures!r}")
assert failures == []
print("FRESH_GENERATED_SEMANTICS_CONCRETE_OK")
