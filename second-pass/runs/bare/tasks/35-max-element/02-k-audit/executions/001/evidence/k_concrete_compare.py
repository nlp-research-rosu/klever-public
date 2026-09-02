#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with two independent Python runs."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable

PROGRAM = Path("/tmp/audit-work/candidate-src/solution.mpy")
DEFINITION = Path("/tmp/audit-work/semantic-llvm-kompiled")
CANONICAL = Path("/reference/canonical.py")
SOLUTION = Path("/tmp/audit-work/candidate-src/solution.py")
INPUTS = Path("/audit-output/evidence/k-concrete-inputs.json")

CASES = [
    ("documented_example_1", [1, 2, 3]),
    ("documented_example_2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]),
    ("minimum_length_zero", [0]),
    ("minimum_length_negative", [-9]),
    ("comparison_greater", [2, 3]),
    ("comparison_less", [3, 2]),
    ("comparison_equal", [3, 3]),
    ("maximum_first", [8, 7, 6, 5]),
    ("maximum_last_all_negative", [-5, -2, -1]),
    ("arbitrary_precision", [-(10**80), 10**120, 10**90]),
]


def load_entry(path: Path, name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


def k_list(values: list[int]) -> str:
    return "[" + ", ".join(str(value) for value in values) + "]"


def run_krun(values: list[int]) -> subprocess.CompletedProcess[str]:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cARGS={k_list(values)}",
    ]
    print("COMMAND: " + shlex.join(command))
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f"EXIT_STATUS: {completed.returncode}")
    print("OUTPUT_BEGIN")
    print(completed.stdout.rstrip())
    print("OUTPUT_END")
    return completed


def main() -> None:
    canonical = load_entry(CANONICAL, "trusted_canonical_for_k_compare")
    solution = load_entry(SOLUTION, "submitted_solution_for_k_compare")
    INPUTS.write_text(
        json.dumps(
            {
                "program": str(PROGRAM),
                "definition": str(DEFINITION),
                "cases": [{"name": name, "input": values} for name, values in CASES],
                "outside_domain_probe": [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    failures: list[str] = []
    for name, values in CASES:
        expected_canonical = canonical(list(values))
        expected_solution = solution(list(values))
        completed = run_krun(values)
        match = re.search(r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", completed.stdout)
        actual = int(match.group(1)) if match else None
        completed_k = bool(re.search(r"<k>\s*\.K\s*</k>", completed.stdout))
        print(
            "CASE_RESULT: "
            + json.dumps(
                {
                    "name": name,
                    "input": values,
                    "canonical": expected_canonical,
                    "solution": expected_solution,
                    "k": actual,
                    "k_cell_complete": completed_k,
                },
                sort_keys=True,
            )
        )
        if (
            completed.returncode != 0
            or actual != expected_canonical
            or actual != expected_solution
            or not completed_k
        ):
            failures.append(name)

    print("OUTSIDE_DOMAIN_PROBE: empty IntSeq is intentionally unrepresentable")
    empty = run_krun([])
    if empty.returncode == 0:
        failures.append("empty_was_accepted")

    print(f"in_domain_case_count={len(CASES)}")
    print(f"failures={json.dumps(failures)}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
