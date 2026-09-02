#!/usr/bin/env python3
"""Concrete false-result witness for the over-broad `%` semantic rule."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import sys


SCRATCH = Path("/tmp/audit-work/121-solution-audit")
SOURCE = Path("/audit-output/evidence/solution_mod_rule_witness.py")
TRANSLATED = SCRATCH / "solution-mod-rule-witness.mpy"
DEFINITION = SCRATCH / "candidate/semantic-audit-kompiled"


def load_solution(path: Path):
    spec = importlib.util.spec_from_file_location("mod_rule_witness_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


def main() -> int:
    command = [
        "krun",
        str(TRANSLATED),
        "--definition",
        str(DEFINITION),
        "-cINPUT=cons(-2,nil)",
    ]
    print("$ " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=SCRATCH / "candidate",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout.rstrip())
    print(f"[exit {completed.returncode}]")
    match = re.search(r"result\s*\(\s*(-?[0-9]+)\s*\)", completed.stdout)
    k_result = int(match.group(1)) if match else None
    python_result = load_solution(SOURCE)([-2])
    print("witness source: sum([x for x in lst[::2] if 1 % x != 1])")
    print("witness input: [-2] (valid non-empty list of integers)")
    print(f"Python: 1 % -2 = {1 % -2}; function result={python_result}")
    print("K rule: 1 modInt -2 = 1; filter is false")
    print(f"generated-semantics result={k_result}")
    false_conclusion = completed.returncode == 0 and k_result != python_result
    print(f"false_semantic_conclusion_witnessed={false_conclusion}")
    return 0 if false_conclusion else 1


if __name__ == "__main__":
    sys.exit(main())
