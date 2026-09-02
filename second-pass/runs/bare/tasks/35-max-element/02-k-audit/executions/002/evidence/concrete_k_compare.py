#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys


WORK = Path("/tmp/audit-work/35-max-element")
DEFINITION = WORK / "audit-semantic-kompiled"


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


def k_int_seq(values: list[int]) -> str:
    return "[" + ", ".join(str(value) for value in values) + "]"


def main() -> int:
    canonical = load_function("fresh_compare_canonical", Path("/reference/canonical.py"))
    candidate = load_function("fresh_compare_candidate", WORK / "solution.py")

    cases = [
        [1],
        [-1],
        [0],
        [1, 2],
        [2, 1],
        [1, 1],
        [-3, -2, -1],
        [-1, -2, -3],
        [0, 0, 0],
        [3, 1, 3, 2],
        [-(10**80), 0, 10**80],
        [10**80, 0, -(10**80)],
        [1, 2, 3],
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
    ]
    rng = random.Random(351337)
    for _ in range(20):
        cases.append([rng.randint(-10**9, 10**9) for _ in range(rng.randint(1, 20))])

    failures = []
    records = []
    for index, values in enumerate(cases):
        command = [
            "krun",
            str(WORK / "solution.mpy"),
            "--definition",
            str(DEFINITION),
            "--color",
            "off",
            f"-cARGS={k_int_seq(values)}",
        ]
        run = subprocess.run(command, text=True, capture_output=True)
        match = re.search(
            r"<result>\s*result\s*\(\s*(-?[0-9]+)\s*\)\s*</result>",
            run.stdout,
            flags=re.DOTALL,
        )
        k_value = int(match.group(1)) if match else None
        canonical_value = canonical(values.copy())
        candidate_value = candidate(values.copy())
        final_k = bool(re.search(r"<k>\s*\.K\s*</k>", run.stdout, flags=re.DOTALL))
        ok = (
            run.returncode == 0
            and final_k
            and k_value == canonical_value
            and k_value == candidate_value
        )
        record = {
            "index": index,
            "input": values,
            "command": command,
            "exit": run.returncode,
            "k_final_dotk": final_k,
            "k_result": k_value,
            "canonical_result": canonical_value,
            "candidate_result": candidate_value,
            "ok": ok,
        }
        records.append(record)
        if not ok:
            record["stdout"] = run.stdout
            record["stderr"] = run.stderr
            failures.append(record)

    print(
        json.dumps(
            {
                "definition": str(DEFINITION),
                "case_count": len(cases),
                "mismatch_count": len(failures),
                "cases": records,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
