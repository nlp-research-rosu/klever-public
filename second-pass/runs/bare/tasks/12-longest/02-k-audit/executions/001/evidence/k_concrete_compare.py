#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
from pathlib import Path
from typing import Callable, Optional


WORK = Path("/tmp/audit-work/12-longest-audit")
DEFINITION = WORK / "semantic-concrete-search-kompiled"


def load_longest(path: Path, name: str) -> Callable[[list[str]], Optional[str]]:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def list_value(strings: list[str]) -> str:
    return "listVal(" + ",".join(f"strVal({q(s)})" for s in strings) + ")"


def out_value(value: Optional[str]) -> str:
    return "noneVal" if value is None else f"strVal({q(value)})"


canonical = load_longest(WORK / "canonical.py", "trusted_canonical_for_k")
candidate = load_longest(WORK / "solution.py", "candidate_solution_for_k")

cases = [
    [],
    [""],
    ["a"],
    ["a", "b", "c"],
    ["a", "bb", "ccc"],
    ["aa", "b", "cc"],
    ["", "a", ""],
    ["é", "e\u0301", "😀😀", "zz"],
]

for index, strings in enumerate(cases):
    oracle = canonical(strings)
    subject = candidate(strings)
    if oracle != subject:
        raise AssertionError((strings, oracle, subject))
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        "-cARGS=" + list_value(strings),
        "--pattern",
        f"<out> {out_value(oracle)} </out>",
        "--output",
        "pretty",
    ]
    print(f"CASE {index}: input={strings!r}")
    print(f"PYTHON canonical={oracle!r} candidate={subject!r}")
    print("$ " + shlex.join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    print(f"KRUN_EXIT_STATUS={completed.returncode}")
    if completed.returncode != 0 or completed.stdout.strip() != "#Top":
        raise SystemExit(1)

print(f"CONCRETE_CASES={len(cases)}")
print("K_VS_PYTHON_RESULT=PASS")
