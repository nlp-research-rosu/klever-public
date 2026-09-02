#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


root = Path("/tmp/audit-work/96-count-up-to")
canonical = load(root / "trusted/canonical.py", "concrete_trusted_canonical")
candidate = load(root / "candidate/solution.py", "concrete_candidate")
program = root / "candidate/solution.mpy"
definition = root / "build/semantic-kompiled"
inputs = [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 18, 20, 25, 49, 50, 97]

records = []
for n in inputs:
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cN={n}",
        "--output",
        "pretty",
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(command, capture_output=True, text=True)
    print("EXIT_STATUS:", completed.returncode)
    if completed.stderr:
        print("STDERR:", completed.stderr.rstrip())
    assert completed.returncode == 0
    result_match = re.search(
        r"<result>\s*(.*?)\s*</result>", completed.stdout, re.DOTALL
    )
    assert result_match, completed.stdout
    result_cell = result_match.group(1)
    k_values = [
        int(value)
        for value in re.findall(r"\bcons\s*\(\s*(-?\d+)\s*,", result_cell)
    ]
    canonical_value = canonical.count_up_to(n)
    candidate_value = candidate.count_up_to(n)
    assert k_values == canonical_value == candidate_value, (
        n,
        k_values,
        canonical_value,
        candidate_value,
    )
    records.append(
        {
            "n": n,
            "k": k_values,
            "canonical": canonical_value,
            "candidate": candidate_value,
        }
    )

print(
    json.dumps(
        {"input_count": len(inputs), "mismatch_count": 0, "records": records},
        indent=2,
        sort_keys=True,
    )
)
