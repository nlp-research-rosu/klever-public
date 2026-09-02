#!/usr/bin/env python3
"""Run fresh K semantics and compare each result with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


def as_int_list(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value},{result})"
    return result


def parse_result(stdout: str):
    match = re.search(r"<result>\s*(.*?)\s*</result>", stdout, re.DOTALL)
    if not match:
        raise ValueError("no <result> cell in krun output")
    rendered = match.group(1).strip()
    if rendered == "none":
        return None
    if re.fullmatch(r"-?[0-9]+", rendered):
        return int(rendered)
    raise ValueError(f"unexpected result term: {rendered!r}")


def main() -> int:
    if len(sys.argv) != 6:
        print(
            "usage: concrete_compare.py SOLUTION.mpy DEFINITION "
            "CANONICAL.py SOLUTION.py RESULTS.json",
            file=sys.stderr,
        )
        return 2
    program, definition, canonical_py, solution_py, results_json = map(
        Path, sys.argv[1:]
    )
    canonical = load_entry(canonical_py, "concrete_trusted_canonical")
    generated = load_entry(solution_py, "concrete_submitted_solution")
    cases = [
        ("documented-ascending", [1, 2, 3, 4, 5]),
        ("documented-permutation", [5, 1, 4, 3, 2]),
        ("empty", []),
        ("duplicates-only", [1, 1]),
        ("singleton", [7]),
        ("two-distinct-ascending", [1, 2]),
        ("two-distinct-descending", [2, 1]),
        ("negative-duplicates", [-1, -4, -4, -2]),
        ("mixed-duplicates", [2, 2, 1, 3, 1]),
        ("large-integers", [10**30, -(10**30), 0]),
    ]

    rows = []
    failures = 0
    for name, values in cases:
        command = [
            "krun",
            str(program),
            "--definition",
            str(definition),
            f"-cINPUT={as_int_list(values)}",
            "--output",
            "pretty",
        ]
        print("$ " + shlex.join(command), flush=True)
        completed = subprocess.run(command, text=True, capture_output=True)
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        print(f"[exit {completed.returncode}]", flush=True)

        expected = canonical(values.copy())
        python_result = generated(values.copy())
        try:
            k_result = parse_result(completed.stdout) if completed.returncode == 0 else None
            parse_error = None
        except ValueError as err:
            k_result = None
            parse_error = str(err)
        matched = (
            completed.returncode == 0
            and parse_error is None
            and type(k_result) is type(expected)
            and k_result == expected
            and type(python_result) is type(expected)
            and python_result == expected
        )
        failures += int(not matched)
        row = {
            "name": name,
            "input": values,
            "input_term": as_int_list(values),
            "canonical": expected,
            "solution_python": python_result,
            "k_result": k_result,
            "krun_exit": completed.returncode,
            "parse_error": parse_error,
            "matched": matched,
        }
        rows.append(row)
        print("comparison=" + json.dumps(row, sort_keys=True), flush=True)

    report = {"case_count": len(rows), "failure_count": failures, "cases": rows}
    results_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"case_count": len(rows), "failure_count": failures}, indent=2
        ),
        flush=True,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
