#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "differential_inputs.json"
PROGRAM = Path("/tmp/audit-work/candidate-src/solution.mpy")
DEFINITION = Path("/tmp/audit-work/semantic-llvm-kompiled")
CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-src/solution.py")


def load_solution(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


def k_ints(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value},{term})"
    return term


def main() -> int:
    explicit_cases = json.loads(MANIFEST.read_text(encoding="utf-8"))[
        "explicit_cases"
    ]
    canonical = load_solution("semantic_test_canonical", CANONICAL_PATH)
    candidate = load_solution("semantic_test_candidate", CANDIDATE_PATH)
    results = []
    failures = []

    for index, values in enumerate(explicit_cases):
        command = [
            "krun",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={k_ints(values)}",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        match = re.search(r"result\s*\(\s*(-?\d+)\s*\)", completed.stdout)
        k_result = int(match.group(1)) if match else None
        canonical_result = canonical(values)
        candidate_result = candidate(values)
        passed = (
            completed.returncode == 0
            and k_result == canonical_result
            and k_result == candidate_result
        )
        record = {
            "index": index,
            "input": values,
            "command": command,
            "exit_status": completed.returncode,
            "k_result": k_result,
            "canonical_result": canonical_result,
            "candidate_result": candidate_result,
            "passed": passed,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        results.append(record)
        if not passed:
            failures.append(record)

    print(
        json.dumps(
            {
                "program": str(PROGRAM),
                "definition": str(DEFINITION),
                "case_count": len(results),
                "failure_count": len(failures),
                "results": results,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
