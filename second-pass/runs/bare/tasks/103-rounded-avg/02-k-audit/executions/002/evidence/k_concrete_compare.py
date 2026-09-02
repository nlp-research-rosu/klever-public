#!/usr/bin/env python3
"""Compare a freshly built generated K semantics with independent Python execution."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess


WORK = Path("/tmp/audit-work/reconstruction")
PROGRAM = WORK / "regenerated-solution.mpy"
DEFINITION = WORK / "concrete-kompiled"


def load_candidate():
    spec = importlib.util.spec_from_file_location("candidate_for_k_compare", WORK / "solution.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


candidate = load_candidate()


def python_outcome(n: int, m: int):
    try:
        value = candidate(n, m)
    except Exception as error:
        return ("raise", type(error).__name__, str(error))
    if isinstance(value, int):
        return ("return", "intVal", value)
    assert isinstance(value, str) and value.startswith(("0b", "-0b"))
    return ("return", "binVal", int(value, 2))


def k_outcome(n: int, m: int):
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cN={n}",
        f"-cM={m}",
    ]
    print("$ " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(completed.stdout.rstrip())
    print(f"KRUN_EXIT_STATUS={completed.returncode}")
    match = re.search(
        r"result \( (binVal|intVal) \( (-?[0-9]+) \) \)",
        completed.stdout,
    )
    if completed.returncode != 0:
        return ("krun-failure", completed.returncode)
    if match is None:
        return ("unparsed", completed.stdout)
    return ("return", match.group(1), int(match.group(2)))


cases = [
    (1, 5),
    (7, 5),
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (2**53 - 1, 2**53 - 1),
    (2**53, 2**53),
    (2**53 + 1, 2**53 + 1),
    (2**53 + 3, 2**53 + 3),
    (10**309, 10**309),
]

mismatches = 0
for n, m in cases:
    py = python_outcome(n, m)
    kval = k_outcome(n, m)
    equal = py == kval
    mismatches += int(not equal)
    print(f"COMPARE n={n} m={m} python={py!r} k={kval!r} equal={equal}")

print(f"SUMMARY cases={len(cases)} mismatches={mismatches}")
# This experiment is expected to expose the unbounded-integer/Float mismatch.
raise SystemExit(0 if mismatches > 0 else 1)
