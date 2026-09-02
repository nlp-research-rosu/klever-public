#!/usr/bin/env python3
"""Compare fresh K concrete execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "semantic-haskell-fresh-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


def find_cell(term, label_name: str):
    if isinstance(term, dict):
        label = term.get("label")
        if isinstance(label, dict) and label.get("name") == label_name:
            return term
        for value in term.values():
            found = find_cell(value, label_name)
            if found is not None:
                return found
    elif isinstance(term, list):
        for value in term:
            found = find_cell(value, label_name)
            if found is not None:
                return found
    return None


def k_result(text: str) -> tuple[int, list[str]]:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={json.dumps(text)}",
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"krun failed code={completed.returncode} "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    document = json.loads(completed.stdout)
    cell = find_cell(document["term"], "<result>")
    if cell is None:
        raise RuntimeError("fresh K result has no <result> cell")
    token = cell["args"][0]
    return int(token["token"]), command


canonical = load_entry("trusted_canonical_kcheck", Path("/reference/canonical.py"))
submitted = load_entry("submitted_python_kcheck", WORK / "solution.py")

cases = [
    "",
    "Hello world",
    "The sky is blue. The sun is shining. I love this weather",
    "I ",
    " I agree",
    "I agree",
    "It is cold",
    "I a. I b",
    "I a? I b",
    "I a! I b",
    "... ! ?  . I count!",
    "\tI tabbed.\nI newline?\rNot me!",
    "I first! No. I second?",
]

k_subject_mismatches = 0
k_canonical_mismatches = 0
print(f"fresh_definition={DEFINITION}")
print("program=/tmp/audit-work/reconstruction/solution.mpy")
for text in cases:
    got_k, command = k_result(text)
    got_submitted = submitted(text)
    got_canonical = canonical(text)
    print(f"COMMAND: {' '.join(command)}")
    print(
        f"input={text!r} K={got_k} "
        f"submitted_python={got_submitted} canonical_python={got_canonical}"
    )
    if got_k != got_submitted:
        k_subject_mismatches += 1
    if got_k != got_canonical:
        k_canonical_mismatches += 1

print(f"case_count={len(cases)}")
print(f"K_vs_submitted_mismatch_count={k_subject_mismatches}")
print(f"K_vs_canonical_mismatch_count={k_canonical_mismatches}")
raise SystemExit(1 if k_subject_mismatches else 0)
