#!/usr/bin/env python3
"""Run fresh generated semantics and compare final results with Python."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path


sys.dont_write_bytecode = True
EVIDENCE = Path("/audit-output/evidence")
SOURCE = Path("/tmp/audit-work/candidate-src")
DEFINITION = Path("/tmp/audit-work/build-concrete/semantic-kompiled")


def load_solution():
    spec = importlib.util.spec_from_file_location(
        "fresh_generated_solution", SOURCE / "solution.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def k_value(value: int) -> str:
    return f"vInt({value})"


def k_list(values: list[str]) -> str:
    return "vList(" + "".join(f"ListItem({value})" for value in values) + ")"


def k_grid(grid: list[list[int]]) -> str:
    return k_list([k_list([k_value(value) for value in row]) for row in grid])


def main() -> None:
    solution = load_solution()
    cases = [
        ("prompt-example-1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3),
        ("prompt-example-2-k1", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1),
        ("n2-bottom-right-k2", [[4, 3], [2, 1]], 2),
        ("n2-top-right-k7", [[4, 1], [3, 2]], 7),
        ("n3-interior-k6", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 6),
        (
            "n4-interior-k10",
            [[16, 15, 14, 13], [12, 1, 9, 10], [11, 2, 8, 7], [6, 5, 4, 3]],
            10,
        ),
    ]
    records = []
    for index, (label, grid, k) in enumerate(cases, 1):
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f"-cGRID={k_grid(grid)}",
            f"-cKLEN={k}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=SOURCE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            timeout=120,
        )
        output_path = EVIDENCE / f"03_krun_case_{index:02d}.out"
        output_path.write_text(completed.stdout)
        match = re.search(r"<result>(.*?)</result>", completed.stdout, re.DOTALL)
        assert match is not None, f"missing result cell in {label}"
        k_result = [
            int(value)
            for value in re.findall(r"vInt\s*\(\s*(-?\d+)\s*\)", match.group(1))
        ]
        python_result = solution(grid, k)
        record = {
            "label": label,
            "grid": grid,
            "k": k,
            "command": shlex.join(command),
            "exit_status": completed.returncode,
            "output_path": str(output_path),
            "python_result": python_result,
            "k_result": k_result,
            "match": k_result == python_result,
        }
        records.append(record)
        print(json.dumps(record, sort_keys=True))
        assert completed.returncode == 0
        assert "<k>\n    .K\n  </k>" in completed.stdout
        assert k_result == python_result
    records_path = EVIDENCE / "03_semantics_cases.json"
    records_path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    print(f"case_count={len(records)}")
    print(f"mismatch_count={sum(not record['match'] for record in records)}")
    print("FRESH_SEMANTICS_DIFFERENTIAL_OK")


if __name__ == "__main__":
    main()
