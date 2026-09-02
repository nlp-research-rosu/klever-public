#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with Python results."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/candidate-src")


def load_min_path() -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location("candidate_concrete", WORK / "solution.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def grid_term(grid: list[list[int]]) -> str:
    rows = [
        (
            "vList("
            + (" ".join(f"ListItem(vInt({value}))" for value in row) or ".List")
            + ")"
        )
        for row in grid
    ]
    return "vList(" + (" ".join(f"ListItem({row})" for row in rows) or ".List") + ")"


def parse_result(stdout: str) -> tuple[list[int], str]:
    match = re.search(r"<result>\s*(.*?)\s*</result>", stdout, flags=re.DOTALL)
    if match is None:
        raise ValueError("krun output has no result cell")
    result_cell = " ".join(match.group(1).split())
    if not result_cell.startswith("some"):
        raise ValueError(f"unexpected result cell: {result_cell}")
    values = [int(value) for value in re.findall(r"vInt\s*\(\s*(-?\d+)\s*\)", result_cell)]
    return values, result_cell


def main() -> int:
    min_path = load_min_path()
    cases = [
        ("prompt-1", "valid", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3),
        ("prompt-2-k1", "valid", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1),
        ("interior-long", "valid", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 6),
        ("corner-top-left", "valid", [[1, 2], [3, 4]], 5),
        ("corner-top-right", "valid", [[2, 1], [3, 4]], 5),
        ("corner-bottom-left", "valid", [[2, 3], [1, 4]], 5),
        ("corner-bottom-right", "valid", [[2, 3], [4, 1]], 5),
        ("zero-answer-loop", "outside-k-domain", [[1, 2], [3, 4]], 0),
        ("n-one", "outside-n-domain", [[1]], 1),
        ("empty-grid", "outside-n-domain", [], 1),
    ]
    failures = []
    print(f"DEFINITION={WORK / 'semantic-kompiled-fresh'}")
    for label, domain, grid, k in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "semantic-kompiled-fresh",
            f"-cGRID={grid_term(grid)}",
            f"-cKLEN={k}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"CASE={label}|DOMAIN={domain}")
        print(f"KRUN_COMMAND={shlex.join(command)}")
        print(f"KRUN_EXIT={completed.returncode}")
        if completed.returncode == 0:
            k_result, raw_result = parse_result(completed.stdout)
            python_result = min_path([row[:] for row in grid], k)
            print(f"K_RESULT_CELL={raw_result}")
            print(f"K_RESULT={k_result}")
            print(f"PYTHON_RESULT={python_result}")
            print(f"MATCH={k_result == python_result}")
            if k_result != python_result:
                failures.append((label, k_result, python_result))
        else:
            output_lines = completed.stdout.splitlines()
            print("KRUN_FAILURE_HEAD=" + repr(output_lines[:20]))
            failures.append((label, "krun-exit", completed.returncode))
    print(f"TOTAL_CASES={len(cases)}")
    print(f"FAILURES={failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
