#!/usr/bin/env python3
"""Run freshly built K semantics and compare its result with both Python files."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def outcome(fn, value: str):
    try:
        return ("value", fn(value))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def k_result(output: str) -> int:
    match = re.search(r"<k>\s*intVal\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K\s*</k>", output)
    if match is None:
        raise AssertionError(f"no final intVal in K output:\n{output}")
    return int(match.group(1))


canonical = load_function("trusted_canonical_kcmp", Path("/reference/canonical.py"))
generated = load_function(
    "scratch_generated_kcmp", Path("/tmp/audit-work/candidate-src/solution.py")
)
cases = [
    "abcde",
    "ACEDY",
    "",
    "a",
    "y",
    "Y",
    "b",
    "ay",
    "ya",
    "yy",
    "rhythm",
    "rhythmy",
    "é",
    "😀",
    "😀a",
    "a😀y",
    "éy",
    "a\nY",
    '"ay',
    "\\y",
]

failures = []
for value in cases:
    command = [
        "krun",
        "/tmp/audit-work/candidate-src/solution.mpy",
        "--definition",
        "/tmp/audit-work/semantic-fresh-kompiled",
        # K String literals accept UTF-8 scalar text.  Python's ensure_ascii
        # surrogate-pair form is not a legal K Unicode escape for astral chars.
        f"-cINPUT={json.dumps(value, ensure_ascii=False)}",
        "--output",
        "pretty",
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True, timeout=120)
    print("EXIT:", completed.returncode)
    if completed.stderr:
        print("STDERR:")
        print(completed.stderr[:4000])
    print("K-CELL:")
    k_cell = re.search(r"<k>.*?</k>", completed.stdout, re.DOTALL)
    print(k_cell.group(0) if k_cell else completed.stdout[:4000])
    py = outcome(generated, value)
    can = outcome(canonical, value)
    if completed.returncode == 0:
        try:
            kval = k_result(completed.stdout)
        except AssertionError as exc:
            failures.append((value, str(exc)))
            kval = None
    else:
        failures.append((value, f"krun exit {completed.returncode}"))
        kval = None
    print(
        "COMPARE:",
        json.dumps(
            {
                "input": value,
                "k": kval,
                "candidate_python": py,
                "canonical_python": can,
            },
            ensure_ascii=False,
        ),
    )
    if py[0] != "value" or kval != py[1]:
        failures.append((value, f"K={kval!r} generated={py!r}"))

print(f"case_count={len(cases)}")
print(f"failure_count={len(failures)}")
for failure in failures:
    print("FAILURE:", failure)
if failures:
    raise SystemExit(1)
