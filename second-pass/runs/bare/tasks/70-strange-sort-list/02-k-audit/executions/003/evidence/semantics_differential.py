#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with two Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strange_sort_list


def plist(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def parse_result(output: str) -> list[int]:
    match = re.search(r"<result>\s*pList\s*\((.*?)\)\s*</result>", output, re.S)
    assert match is not None, output
    tokens = re.findall(r"cons|-?\d+|nil|[(),]", match.group(1))
    position = 0

    def parse_list() -> list[int]:
        nonlocal position
        if tokens[position] == "nil":
            position += 1
            return []
        assert tokens[position] == "cons"
        position += 1
        assert tokens[position] == "("
        position += 1
        value = int(tokens[position])
        position += 1
        assert tokens[position] == ","
        position += 1
        tail = parse_list()
        assert tokens[position] == ")"
        position += 1
        return [value, *tail]

    result = parse_list()
    assert position == len(tokens), (tokens, position)
    return result


canonical = load_function(Path("/reference/canonical.py"), "canonical_for_k")
candidate = load_function(Path("/candidate/solution.py"), "candidate_for_k")
cases = [
    [],
    [-7],
    [2, 1],
    [1, 2, 3, 4],
    [3, -1, 2, 3, 0],
    [9, -9, 4, 4, 0, 2],
]

for values in cases:
    command = [
        "krun",
        "/tmp/audit-work/candidate-src/solution.mpy",
        "--definition",
        "/tmp/audit-work/concrete-kompiled",
        '-cENTRY="strange_sort_list"',
        f"-cINPUT={plist(values)}",
    ]
    completed = subprocess.run(
        command, check=False, capture_output=True, text=True, timeout=30
    )
    assert completed.returncode == 0, (command, completed.stdout, completed.stderr)
    k_result = parse_result(completed.stdout)
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    print(
        f"input={values!r} k={k_result!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r}"
    )
    assert k_result == canonical_result == candidate_result

print(f"SEMANTICS DIFFERENTIAL PASS cases={len(cases)}")
