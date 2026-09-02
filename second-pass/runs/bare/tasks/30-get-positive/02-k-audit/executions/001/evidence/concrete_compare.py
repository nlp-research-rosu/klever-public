#!/usr/bin/env python3
"""Run the freshly compiled generated K semantics and compare with Python."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/30-get-positive")


def load_function(path: Path, name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


def pylist(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def find_cell(term: dict[str, Any], cell_name: str) -> dict[str, Any]:
    label = term.get("label", {}).get("name")
    if label == cell_name:
        return term
    for arg in term.get("args", []):
        if isinstance(arg, dict):
            try:
                return find_cell(arg, cell_name)
            except LookupError:
                pass
    for item in term.get("items", []):
        if isinstance(item, dict):
            try:
                return find_cell(item, cell_name)
            except LookupError:
                pass
    raise LookupError(cell_name)


def decode_pylist(term: dict[str, Any]) -> list[int]:
    if term.get("node") == "KSequence":
        items = term["items"]
        assert len(items) == 1, term
        return decode_pylist(items[0])
    label = term.get("label", {}).get("name")
    if label == "nil":
        return []
    if label == "cons":
        head, tail = term["args"]
        assert head.get("node") == "KToken" and head["sort"]["name"] == "Int", head
        return [int(head["token"])] + decode_pylist(tail)
    raise AssertionError(f"unexpected K result term: {term}")


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(SCRATCH / "solution.py", "scratch_solution")
cases = [
    ("empty", []),
    ("zero", [0]),
    ("branch-boundary", [-1, 0, 1]),
    ("prompt-example-1", [-1, 2, -4, 5, 6]),
    ("prompt-example-2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]),
    ("duplicates-and-order", [2, -1, 2, 0, 3, 2]),
    ("large-mathematical-int", [-(10**100), 0, 10**100]),
]

mismatches = []
for label, values in cases:
    command = [
        "/usr/bin/krun",
        str(SCRATCH / "solution.mpy"),
        "--definition",
        str(SCRATCH / "concrete-kompiled"),
        f"-cINPUT={pylist(values)}",
        "--output",
        "json",
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    if completed.stderr:
        print(f"KRUN_STDERR: {completed.stderr.rstrip()}")
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    document = json.loads(completed.stdout)
    k_cell = find_cell(document["term"], "<k>")
    k_result = decode_pylist(k_cell["args"][0])
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    match = k_result == canonical_result == candidate_result
    print(
        f"CASE {label} input={values!r} k={k_result!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r} "
        f"match={match}"
    )
    if not match:
        mismatches.append(label)

print(f"SUMMARY cases={len(cases)} mismatches={len(mismatches)}")
raise SystemExit(1 if mismatches else 0)
