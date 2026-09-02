#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python functions."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/87-get-row")
PROGRAM = SCRATCH / "source" / "solution.mpy"
DEFINITION = SCRATCH / "semantic-audit-kompiled"


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


canonical = load_entry(Path("/reference/canonical.py"), "semantics_oracle")
candidate = load_entry(SCRATCH / "source" / "solution.py", "semantics_candidate")


def vlist(items):
    result = "vnil"
    for item in reversed(items):
        result = f"vcons({item},{result})"
    return result


def py_value(value):
    if isinstance(value, int):
        return f"pyInt({value})"
    if isinstance(value, tuple):
        return f"pyTuple({vlist([py_value(x) for x in value])})"
    if isinstance(value, list):
        return f"pyList({vlist([py_value(x) for x in value])})"
    raise TypeError(value)


def compact(text):
    return re.sub(r"\s+", "", text)


cases = [
    ("normal-multiple", [[1, 2, 1], [1]], 1),
    (
        "documented-prompt",
        [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 1, 6],
            [1, 2, 3, 4, 5, 1],
        ],
        1,
    ),
    ("empty-outer", [], 1),
    ("empty-and-hit", [[], [1], [1, 2, 3]], 3),
    ("singleton-hit", [[0]], 0),
    ("singleton-miss", [[0]], 1),
    ("ragged-negative", [[-2, -1, 0], [], [1, -1]], -1),
]

failures = []
for name, matrix, x in cases:
    expected = canonical(matrix, x)
    candidate_result = candidate(matrix, x)
    expected_k = f"<result>returned(pyList({vlist([py_value(t) for t in expected])}))</result>"
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cLST={py_value(matrix)}",
        f"-cX={py_value(x)}",
        "--output",
        "pretty",
    ]
    print(f"CASE {name}")
    print("$", shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True)
    normalized = compact(completed.stdout)
    match = re.search(r"<result>.*?</result>", normalized)
    observed_k = match.group(0) if match else "<missing-result-cell>"
    print(f"exit={completed.returncode}")
    print(f"python_canonical={expected!r}")
    print(f"python_candidate={candidate_result!r}")
    print(f"expected_k={expected_k}")
    print(f"observed_k={observed_k}")
    if completed.stderr:
        print("stderr=" + completed.stderr.rstrip())
    ok = (
        completed.returncode == 0
        and candidate_result == expected
        and observed_k == expected_k
        and "<k>.K</k>" in normalized
    )
    print(f"case_ok={int(ok)}")
    if not ok:
        failures.append(name)

print(f"case_count={len(cases)}")
print(f"failure_count={len(failures)}")
if failures:
    print("failures=" + ",".join(failures))
    raise SystemExit(1)
