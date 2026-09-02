#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with trusted Python results."""

from __future__ import annotations

import importlib.util
import shlex
import subprocess
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/22-filter-integers/src")
CANONICAL_PATH = Path("/reference/canonical.py")


def load_canonical(path: Path) -> Callable[[list[Any]], list[int]]:
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


class Opaque:
    pass


cases: list[tuple[str, str, list[Any]]] = [
    (
        "prompt_example_1",
        'VList(VString("a"), VFloat("3.14"), VInt(5))',
        ["a", 3.14, 5],
    ),
    (
        "prompt_example_2",
        'VList(VInt(1), VInt(2), VInt(3), VString("abc"), '
        "VDict, VList())",
        [1, 2, 3, "abc", {}, []],
    ),
    ("empty", "VList()", []),
    (
        "bool_int_boundary",
        'VList(VBool(true), VBool(false), VInt(0), VInt(-4), VFloat("2.0"))',
        [True, False, 0, -4, 2.0],
    ),
    (
        "all_runtime_constructors",
        'VList(VString("x"), VFloat("-0.0"), VInt(-2), VBool(true), '
        'VList(VInt(9)), VDict, VNone, VOpaque("custom"), VInt(4))',
        ["x", -0.0, -2, True, [9], {}, None, Opaque(), 4],
    ),
    (
        "duplicates_and_order",
        'VList(VInt(2), VString("skip"), VInt(2), VBool(false), '
        'VInt(-1), VFloat("2.0"))',
        [2, "skip", 2, False, -1, 2.0],
    ),
]


def as_k_list(values: list[int]) -> str:
    items: list[str] = []
    for value in values:
        if type(value) is bool:
            items.append(f"VBool({str(value).lower()})")
        elif type(value) is int:
            items.append(f"VInt({value})")
        else:
            raise AssertionError(f"trusted oracle returned non-int value: {value!r}")
    body = ",".join(items)
    if body:
        body += ","
    return f"VList({body}.PyVals)"


canonical = load_canonical(CANONICAL_PATH)
mismatches = 0
for name, k_input, python_input in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "fresh-semantic-kompiled",
        f"-cINPUT={k_input}",
    ]
    print(f"CASE: {name}")
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout.rstrip())
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    expected_value = as_k_list(canonical(python_input))
    expected_fragment = f"<return>result({expected_value})</return>"
    normalized = "".join(completed.stdout.split())
    matched = completed.returncode == 0 and expected_fragment in normalized
    print(f"TRUSTED_PYTHON_EXPECTED: {expected_value}")
    print(f"MATCH: {str(matched).lower()}")
    if not matched:
        mismatches += 1

print(f"SUMMARY: cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
