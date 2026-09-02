#!/usr/bin/env python3
"""Fresh generated-semantics executions compared with both Python programs."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/43-pairs-sum-to-zero")
CANDIDATE = ROOT / "candidate"
DEFINITION = ROOT / "concrete-kompiled"


def load(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


def py_outcome(function: Callable[[list[int]], bool], values: list[int]) -> dict[str, object]:
    try:
        return {"kind": "return", "value": function(values.copy())}
    except BaseException as error:
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


def iseq(values: list[int]) -> str:
    if not values:
        return ".ISeq"
    return " :: ".join(str(value) for value in values) + " :: .ISeq"


def main() -> int:
    canonical = load(ROOT / "trusted/canonical.py", "trusted_canonical_k_compare")
    candidate = load(CANDIDATE / "solution.py", "candidate_solution_k_compare")
    cases = [
        ("empty", []),
        ("singleton_zero", [0]),
        ("two_zeroes", [0, 0]),
        ("recursive_false", [1, 2, 3, 7]),
        ("recursive_true", [2, 4, -5, 3, 5, 7]),
        ("large_integer_true", [10**100, 1, -(10**100)]),
        ("recursion_boundary_false", [1] * 997),
        ("recursion_boundary_early_true", [1, -1] + [1] * 995),
    ]
    failures = 0
    semantic_candidate_mismatches = 0
    for name, values in cases:
        command = [
            "krun",
            str(CANDIDATE / "solution.mpy"),
            "--definition",
            str(DEFINITION),
            f"-cINPUT={iseq(values)}",
            "--output",
            "pretty",
        ]
        completed = subprocess.run(
            command,
            cwd=CANDIDATE,
            text=True,
            capture_output=True,
            timeout=180,
        )
        k_result: object
        if "pyBool ( true )" in completed.stdout:
            k_result = True
        elif "pyBool ( false )" in completed.stdout:
            k_result = False
        else:
            k_result = None
        canonical_result = py_outcome(canonical, values)
        candidate_result = py_outcome(candidate, values)
        record = {
            "name": name,
            "length": len(values),
            "input_prefix": values[:8],
            "input_term_sha256": hashlib.sha256(iseq(values).encode()).hexdigest(),
            "command": command[:4]
            + [f"-cINPUT=<ISeq length {len(values)}>", "--output", "pretty"],
            "krun_exit": completed.returncode,
            "krun_result": k_result,
            "krun_stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
            "krun_stderr": completed.stderr.strip(),
            "canonical_python": canonical_result,
            "candidate_python": candidate_result,
        }
        print("CASE:", json.dumps(record, sort_keys=True))
        if completed.returncode != 0 or k_result is None:
            failures += 1
        if canonical_result.get("kind") == "return" and k_result != canonical_result.get("value"):
            failures += 1
        if (
            candidate_result.get("kind") != "return"
            or k_result != candidate_result.get("value")
        ):
            semantic_candidate_mismatches += 1

    print("CONCRETE_EXECUTION_FAILURES:", failures)
    print("SEMANTICS_VS_CANDIDATE_PYTHON_MISMATCHES:", semantic_candidate_mismatches)
    status = 1 if failures or semantic_candidate_mismatches else 0
    print("CONCRETE_COMPARE_EXIT_STATUS:", status)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
