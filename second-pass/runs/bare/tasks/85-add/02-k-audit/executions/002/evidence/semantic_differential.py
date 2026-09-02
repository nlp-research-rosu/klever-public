#!/usr/bin/env python3
"""Compare fresh generated-semantics executions against both Python functions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path("/tmp/audit-work/85-add-review")
DEFINITION = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "concrete-kompiled"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iseq(values):
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def k_run(values):
    input_term = f"pyList({iseq(values)})"
    command = [
        "krun",
        "solution.mpy",
        f"-cINPUT={input_term}",
        "--definition",
        str(DEFINITION),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    matches = re.findall(r"<k>\s*pyInt \( (-?\d+) \) ~> \.K\s*</k>", completed.stdout)
    parsed = int(matches[0]) if completed.returncode == 0 and len(matches) == 1 else None
    return command, completed.returncode, parsed, completed.stdout


def main() -> int:
    canonical = load("trusted_canonical_sem", ROOT / "canonical.py").add
    candidate = load("generated_candidate_sem", ROOT / "solution.py").add
    cases = [
        [],
        [1],
        [4, 2, 6, 7],
        [1, 2],
        [1, 3],
        [1, 0],
        [-1, -2, -3, -4, -5],
        [8, 5, 4, -6, 2, 12],
        [10**30, -(10**30), 3, 4],
    ]
    mismatches = 0
    for values in cases:
        expected = canonical(list(values))
        generated = candidate(list(values))
        command, status, k_value, output = k_run(values)
        same = status == 0 and expected == generated == k_value
        mismatches += int(not same)
        print(f"INPUT={values!r}")
        print("KRUN_COMMAND=" + " ".join(command))
        print(
            f"CANONICAL={expected} CANDIDATE={generated} K={k_value} "
            f"KRUN_EXIT={status} MATCH={same}"
        )
        if not same:
            print("KRUN_OUTPUT_BEGIN")
            print(output.rstrip())
            print("KRUN_OUTPUT_END")
    print(f"SEMANTIC_CASES={len(cases)}")
    print(f"SEMANTIC_MISMATCHES={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
