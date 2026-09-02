#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import subprocess
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "is_palindrome")


parser = argparse.ArgumentParser()
parser.add_argument("--definition", type=pathlib.Path, required=True)
parser.add_argument("--program", type=pathlib.Path, required=True)
parser.add_argument("--canonical", type=pathlib.Path, required=True)
parser.add_argument("--solution", type=pathlib.Path, required=True)
args = parser.parse_args()

canonical = load_entry(args.canonical, "concrete_trusted_canonical")
solution = load_entry(args.solution, "concrete_candidate_solution")

cases = [
    "",
    "a",
    "aa",
    "ab",
    "aba",
    "abb",
    "abba",
    "abca",
    "abcba",
    "zbcd",
    "été",
    "éaé",
    "🙂a🙂",
    "🙂🙃",
    "a\u0301a",
    "\x00a\x00",
    "\n\t\n",
    "a" * 64,
    "a" * 31 + "b" + "a" * 31,
    "a" * 31 + "bc" + "a" * 31,
]

pattern = re.compile(r"PyBool\s*\(\s*(true|false)\s*\)")
mismatch_count = 0
for index, value in enumerate(cases):
    command = [
        "krun",
        str(args.program),
        "--definition",
        str(args.definition),
        "-cFUNCTION=" + json.dumps("is_palindrome", ensure_ascii=False),
        "-cARG=" + json.dumps(value, ensure_ascii=False),
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    matches = pattern.findall(completed.stdout)
    parsed = matches[-1] == "true" if matches else None
    canonical_result = canonical(value)
    solution_result = solution(value)
    okay = (
        completed.returncode == 0
        and parsed is not None
        and parsed == canonical_result
        and parsed == solution_result
    )
    if not okay:
        mismatch_count += 1
    print(
        json.dumps(
            {
                "index": index,
                "input": value,
                "command": command,
                "krun_exit": completed.returncode,
                "k_result": parsed,
                "canonical_result": canonical_result,
                "solution_result": solution_result,
                "match": okay,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

print(f"case_count={len(cases)}")
print(f"mismatch_count={mismatch_count}")
raise SystemExit(1 if mismatch_count else 0)
