#!/usr/bin/env python3
"""Run fresh LLVM K semantics and compare results with both Python programs."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work/33-sort-third")


def load_entry(path: Path, name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def label(node: dict[str, Any]) -> str:
    return str(node.get("label", {}).get("name", ""))


def find_label(node: Any, wanted: str) -> dict[str, Any] | None:
    if isinstance(node, dict):
        if node.get("node") == "KApply" and label(node) == wanted:
            return node
        for value in node.values():
            found = find_label(value, wanted)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_label(value, wanted)
            if found is not None:
                return found
    return None


def decode_ints(node: dict[str, Any]) -> list[int]:
    out: list[int] = []
    while True:
        current_label = label(node)
        if current_label.startswith(".List{"):
            return out
        if not current_label.startswith("_,__") or len(node.get("args", [])) != 2:
            raise ValueError(f"unexpected Ints node: {json.dumps(node)}")
        head, node = node["args"]
        if head.get("node") != "KToken" or head.get("sort", {}).get("name") != "Int":
            raise ValueError(f"unexpected integer token: {json.dumps(head)}")
        out.append(int(head["token"]))


def decode_result(document: dict[str, Any]) -> list[int]:
    result_cell = find_label(document["term"], "<result>")
    if result_cell is None:
        raise ValueError("no <result> cell")
    sequence = result_cell["args"][0]
    items = sequence.get("items", [])
    if sequence.get("node") != "KSequence" or len(items) != 1:
        raise ValueError(f"result is not a singleton K sequence: {json.dumps(sequence)}")
    value = items[0]
    if label(value) != "VList":
        raise ValueError(f"result is not VList: {json.dumps(value)}")
    return decode_ints(value["args"][0])


def k_input(values: list[int]) -> str:
    return "VList(" + ", ".join(str(value) for value in values) + ")"


def main() -> int:
    canonical = load_entry(WORK / "canonical.py", "stage3_canonical")
    candidate = load_entry(WORK / "solution.py", "stage3_candidate")
    cases = [
        [],
        [9],
        [9, 8],
        [1, 2, 3],
        [9, 8, 7, 6],
        [9, 8, 7, 6, 5, 4],
        [3, 0, 0, 2, 0, 0, 1],
        [1, 0, 0, 2, 0, 0, 3],
        [2, 0, 0, 2, 0, 0, 2],
        [-1, 7, 8, -3, 9, 10, -2],
        [10**40, 1, 2, -(10**40), 3, 4, 0],
    ]

    failures = 0
    for index, values in enumerate(cases):
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "semantic-kompiled",
            f"-cINPUT={k_input(values)}",
            "--output",
            "json",
        ]
        print(f"CASE_{index}_COMMAND={shlex.join(command)}")
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            capture_output=True,
            check=False,
        )
        print(f"CASE_{index}_KRUN_EXIT_STATUS={completed.returncode}")
        if completed.returncode != 0:
            print(completed.stdout)
            print(completed.stderr)
            failures += 1
            continue

        k_result = decode_result(json.loads(completed.stdout))
        canonical_input = list(values)
        candidate_input = list(values)
        canonical_result = canonical(canonical_input)
        candidate_result = candidate(candidate_input)
        passed = (
            k_result == canonical_result == candidate_result
            and canonical_input == values
            and candidate_input == values
        )
        print(
            f"CASE_{index}_RESULT input={values!r} "
            f"k={k_result!r} canonical={canonical_result!r} "
            f"candidate={candidate_result!r} PASS={passed}"
        )
        if not passed:
            failures += 1

    print(f"CASE_COUNT={len(cases)}")
    print(f"FAILURE_COUNT={failures}")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
