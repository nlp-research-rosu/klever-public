#!/usr/bin/env python3
"""Compare freshly compiled K execution with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable


def load_search(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


def python_outcome(fn: Callable[[list[int]], int], values: list[int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(values.copy())}
    except Exception as err:
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def int_seq(values: list[int]) -> str:
    result = ".Ints"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_search(args.canonical, "semantic_audit_canonical")
    candidate = load_search(args.candidate, "semantic_audit_candidate")
    cases = json.loads(args.inputs.read_text())
    failures: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []

    for case in cases:
        values = case["input"]
        k_input = f"VList({int_seq(values)})"
        command = [
            "/usr/bin/krun",
            str(args.program),
            "--definition",
            str(args.definition),
            f"-cINPUT={k_input}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        match = re.search(
            r"<result>\s*VInt\s*\(\s*(-?\d+)\s*\)\s*</result>",
            completed.stdout,
        )
        k_value = int(match.group(1)) if match else None
        candidate_result = python_outcome(candidate, values)
        canonical_result = python_outcome(canonical, values)
        expected_value = (
            candidate_result["value"] if candidate_result["kind"] == "return" else None
        )
        final_k = "<k> .K </k>" in " ".join(completed.stdout.split())
        passed = (
            completed.returncode == 0
            and final_k
            and k_value is not None
            and k_value == expected_value
            and (
                not case["in_domain"]
                or canonical_result
                == {"kind": "return", "value": expected_value}
            )
        )
        record = {
            "name": case["name"],
            "input": values,
            "in_domain": case["in_domain"],
            "command": command,
            "krun_exit": completed.returncode,
            "k_final": final_k,
            "k_result": k_value,
            "candidate": candidate_result,
            "canonical": canonical_result,
            "pass": passed,
            "stderr": completed.stderr[-1000:],
        }
        results.append(record)
        if not passed:
            failures.append(record)

    print(json.dumps({"cases": results, "failure_count": len(failures)}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
