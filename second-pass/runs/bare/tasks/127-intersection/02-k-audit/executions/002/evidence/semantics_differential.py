#!/usr/bin/env python3
"""Compare fresh generated-semantics runs with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/build-concrete/semantic-v2-kompiled")
PROGRAM = Path("/tmp/audit-work/candidate-src/solution.mpy")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


canonical = load_entry(
    Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical_semantics"
)
generated = load_entry(
    Path("/tmp/audit-work/candidate-src/solution.py"), "generated_python_semantics"
)

cases = [
    ("prompt_touch", (1, 2), (2, 3)),
    ("prompt_length_1", (-1, 1), (0, 4)),
    ("prompt_length_2", (-3, -1), (-5, 5)),
    ("degenerate", (0, 0), (0, 0)),
    ("disjoint", (-8, -2), (3, 9)),
    ("length_0", (0, 3), (3, 8)),
    ("length_1", (0, 3), (2, 8)),
    ("prime_2", (0, 3), (1, 8)),
    ("prime_3", (0, 3), (0, 8)),
    ("composite_4", (0, 4), (-8, 8)),
    ("prime_5", (0, 5), (-8, 8)),
    ("composite_9", (0, 9), (-8, 20)),
    ("composite_25", (0, 25), (-8, 40)),
    ("prime_97", (0, 97), (-100, 200)),
    ("spec_case_1", (0, 5), (-2, 7)),
    ("spec_case_2", (0, 5), (-2, 3)),
    ("spec_case_3", (0, 5), (2, 7)),
    ("spec_case_4", (0, 5), (2, 4)),
]


def mpy_tuple(interval: tuple[int, int]) -> str:
    return f"TupleExpr(Int({interval[0]}),Int({interval[1]}))"


failures = []
for label, interval1, interval2 in cases:
    py_canonical = canonical(interval1, interval2)
    py_generated = generated(interval1, interval2)
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cINTERVAL1={mpy_tuple(interval1)}",
        f"-cINTERVAL2={mpy_tuple(interval2)}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    k_match = re.search(
        r'<k>\s*strVal\s*\(\s*"(YES|NO)"\s*\)\s*~>\s*\.K\s*</k>',
        completed.stdout,
        re.DOTALL,
    )
    k_value = k_match.group(1) if k_match else "NO_FINAL_VALUE"
    print("COMMAND:", shlex.join(command))
    print(
        f"CASE={label} input1={interval1} input2={interval2} "
        f"canonical={py_canonical} generated_python={py_generated} "
        f"k={k_value} krun_exit={completed.returncode}"
    )
    if completed.stderr:
        print("KRUN_STDERR:", completed.stderr.strip()[:800])
    if completed.returncode != 0 or not (
        py_canonical == py_generated == k_value
    ):
        failures.append(
            (label, interval1, interval2, py_canonical, py_generated, k_value)
        )

print(f"semantics_cases={len(cases)}")
print(f"semantics_mismatches={len(failures)}")
if failures:
    for failure in failures:
        print("MISMATCH", failure)
    raise SystemExit(1)
