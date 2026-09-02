#!/usr/bin/env python3
"""Execute the rebuilt generated semantics and compare with both Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess


ROOT = Path("/tmp/audit-work/58-common-audit")
CANDIDATE = ROOT / "candidate"
DEFINITION = ROOT / "semantic-kompiled-audit"


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load_entry(ROOT / "trusted" / "canonical.py", "canonical_concrete")
candidate = load_entry(CANDIDATE / "solution.py", "candidate_concrete")

cases = [
    ("prompt-example-1", [1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]),
    ("prompt-example-2", [5, 3, 2, 8], [3, 2]),
    ("both-empty", [], []),
    ("left-empty", [], [1, 1]),
    ("right-empty", [1, 1], []),
    ("singleton-hit", [0], [0]),
    ("singleton-miss", [0], [1]),
    ("duplicate-negative", [3, 3, -1, 2], [3, -1, -1]),
    ("insertion-branches", [4, 1, 3, 2], [3, 4, 2, 1]),
    ("arbitrary-precision", [-(10**50), 0, 10**50], [10**50, -(10**50)]),
]


def k_list(values):
    return "list(" + ",".join(map(str, values)) + ")"


def parse_k_result(output: str):
    match = re.search(
        r"<k>\s*list\s*\(\s*(.*?)\s*\.Ints\s*\)\s*~>\s*\.K\s*</k>",
        output,
        re.DOTALL,
    )
    if match is None:
        raise ValueError("could not find final list in <k> cell")
    return [int(value) for value in re.findall(r"-?[0-9]+", match.group(1))]


failures = []
for label, left, right in cases:
    command = [
        "krun",
        str(CANDIDATE / "solution.mpy"),
        "--definition",
        str(DEFINITION),
        f"-cL1={k_list(left)}",
        f"-cL2={k_list(right)}",
    ]
    print("$", " ".join(repr(piece) if " " in piece else piece for piece in command))
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.rstrip())
    print(f"[exit {result.returncode}]")
    try:
        k_result = parse_k_result(result.stdout)
    except Exception as error:
        k_result = ("parse-error", str(error))
    canonical_result = canonical(left, right)
    candidate_result = candidate(left, right)
    print(
        f"COMPARE {label}: canonical={canonical_result!r} "
        f"candidate={candidate_result!r} K={k_result!r}"
    )
    if (
        result.returncode != 0
        or k_result != canonical_result
        or k_result != candidate_result
    ):
        failures.append(label)

print("CONCRETE_CASES=", len(cases))
print("FAILURES=", failures)
raise SystemExit(bool(failures))
