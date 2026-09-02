#!/usr/bin/env python3
"""Compare fresh LLVM-semantics executions with two independent Python runs."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/61-correct-bracketing-audit")
CANDIDATE = ROOT / "candidate"
DEFINITION = CANDIDATE / "concrete-kompiled"
PROGRAM = (CANDIDATE / "solution.mpy").read_text()


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry(ROOT / "reference" / "canonical.py", "sem_oracle")
generated = load_entry(CANDIDATE / "solution.py", "sem_candidate")

boundaries = [
    "",
    "(",
    ")",
    "()",
    "((",
    "))",
    ")(",
    "()()",
    "(())",
    "(()())",
    ")(()",
    "((()))",
    "(()",
    "())",
    "((())())",
    "()(()())",
]
cases: list[tuple[str, str]] = [("boundary", value) for value in boundaries]
for length in range(6):
    for chars in itertools.product("()", repeat=length):
        cases.append(("exhaustive-0..5", "".join(chars)))
rng = random.Random(610062)
for _ in range(25):
    length = rng.randrange(6, 65)
    cases.append(("seeded-random-6..64", "".join(rng.choice("()") for _ in range(length))))
cases.extend(
    [
        ("long", "(" * 100 + ")" * 100),
        ("long", ")" + "(" * 100 + ")" * 99),
        ("long", "()" * 100),
        ("long", "(" * 200),
    ]
)

result_pattern = re.compile(r"boolVal\s*\(\s*(true|false)\s*\)")
mismatches = []
executions = []
for category, value in cases:
    term = f"Run({PROGRAM}, \"correct_bracketing\", {json.dumps(value)})"
    completed = subprocess.run(
        [
            "krun",
            "--definition",
            str(DEFINITION),
            f"-cPGM={term}",
            "--output",
            "pretty",
        ],
        cwd=CANDIDATE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    match = result_pattern.search(completed.stdout)
    k_result = None if match is None else match.group(1) == "true"
    oracle_result = canonical(value)
    python_result = generated(value)
    row = {
        "category": category,
        "input": value,
        "length": len(value),
        "krun_exit": completed.returncode,
        "k_result": k_result,
        "canonical": oracle_result,
        "generated_python": python_result,
    }
    executions.append(row)
    if (
        completed.returncode != 0
        or match is None
        or k_result != oracle_result
        or k_result != python_result
    ):
        row["krun_output"] = completed.stdout[-4_000:]
        mismatches.append(row)

summary = {
    "definition": str(DEFINITION),
    "program_sha256": "6679593a8ad6af41affa3fe98fe9acd62e1d00f49f869df85c6d414ade518969",
    "boundary_count": len(boundaries),
    "exhaustive_lengths": [0, 5],
    "seed": 610062,
    "seeded_random_count": 25,
    "long_case_lengths": [200, 200, 200, 200],
    "total_krun_executions": len(cases),
    "mismatch_count": len(mismatches),
    "boundary_results": executions[: len(boundaries)],
    "first_mismatches": mismatches[:10],
}
print(json.dumps(summary, indent=2))
raise SystemExit(1 if mismatches else 0)
