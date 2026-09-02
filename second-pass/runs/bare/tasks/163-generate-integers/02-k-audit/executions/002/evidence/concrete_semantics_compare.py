#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess


DEFINITION = "/tmp/audit-work/candidate/semantic-kompiled"
PROGRAM = "/tmp/audit-work/candidate/solution.mpy"


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


canonical = load_entry("/reference/canonical.py", "trusted_canonical_concrete")
candidate = load_entry("/tmp/audit-work/candidate/solution.py", "candidate_concrete")


def label(node: dict) -> str | None:
    item = node.get("label")
    return item.get("name") if isinstance(item, dict) else None


def find_apply(node, wanted: str):
    if isinstance(node, dict):
        if node.get("node") == "KApply" and label(node) == wanted:
            return node
        for value in node.values():
            found = find_apply(value, wanted)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_apply(value, wanted)
            if found is not None:
                return found
    return None


def list_items(node) -> list[int]:
    values: list[int] = []
    if isinstance(node, dict):
        if node.get("node") == "KApply" and label(node) == "ListItem":
            token = node["args"][0]
            assert token["node"] == "KToken" and token["sort"]["name"] == "Int"
            values.append(int(token["token"]))
        else:
            for arg in node.get("args", []):
                values.extend(list_items(arg))
    return values


cases = [
    (2, 8),
    (8, 2),
    (10, 14),
    (1, 1),
    (1, 2),
    (2, 2),
    (3, 4),
    (4, 4),
    (5, 6),
    (6, 6),
    (7, 8),
    (8, 8),
    (9, 9),
    (3, 7),
    (7, 3),
    (1, 10**30),
    (10**30, 1),
]

for a, b in cases:
    command = [
        "krun",
        PROGRAM,
        "--definition",
        DEFINITION,
        f"-cA={a}",
        f"-cB={b}",
        "--output",
        "json",
    ]
    print("COMMAND:", shlex.join(command))
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.stderr:
        print("STDERR:", completed.stderr.rstrip())
    assert completed.returncode == 0
    document = json.loads(completed.stdout)
    result_cell = find_apply(document["term"], "<result>")
    k_cell = find_apply(document["term"], "<k>")
    assert result_cell is not None and k_cell is not None
    assert k_cell["args"][0].get("node") == "KSequence"
    assert k_cell["args"][0].get("arity") == 0
    actual = list_items(result_cell)
    expected_canonical = canonical(a, b)
    expected_candidate = candidate(a, b)
    print(
        f"RESULT input=({a},{b}) "
        f"k={actual} canonical={expected_canonical} candidate={expected_candidate}"
    )
    assert actual == expected_canonical == expected_candidate

print(f"concrete_cases={len(cases)}")
print("CONCRETE_SEMANTICS_COMPARE=PASS")
