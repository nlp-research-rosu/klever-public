#!/usr/bin/env python3
"""Mechanically compare the entry claim's closure with loaded solution.mpy."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
RUNTIME_DEFINITION = SCRATCH / "audit-runtime-kompiled"
PROOF_DEFINITION = SCRATCH / "audit-verification-kompiled"


def extract_balanced(text: str, marker: str) -> str:
    start = text.index(marker)
    depth = 0
    in_string = False
    escaped = False
    for offset, character in enumerate(text[start:], start=start):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : offset + 1]
    raise ValueError(f"unbalanced expression beginning at {marker!r}")


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise SystemExit(completed.returncode)
    return json.loads(completed.stdout)


def find_label(term: object, label_name: str) -> list[dict]:
    found: list[dict] = []
    if isinstance(term, dict):
        label = term.get("label")
        if (
            isinstance(label, dict)
            and label.get("name") == label_name
        ):
            found.append(term)
        for value in term.values():
            found.extend(find_label(value, label_name))
    elif isinstance(term, list):
        for value in term:
            found.extend(find_label(value, label_name))
    return found


spec_text = (SCRATCH / "spec.k").read_text(encoding="utf-8")
spec_closure_text = extract_balanced(spec_text, "closureVal(")

parsed_spec = run_json(
    [
        "kast",
        "--input",
        "rule",
        "--expression",
        f"{spec_closure_text} => {spec_closure_text}",
        "--definition",
        str(PROOF_DEFINITION),
        "--module",
        "VERIFICATION",
        "--output",
        "json",
    ]
)

loaded_module = run_json(
    [
        "krun",
        "solution.mpy",
        "--definition",
        str(RUNTIME_DEFINITION),
        "--output",
        "json",
    ]
)

closure_label = "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
actual_closures = find_label(loaded_module["term"], closure_label)
if len(actual_closures) != 1:
    raise SystemExit(f"expected exactly one loaded closure, got {len(actual_closures)}")

spec_term = parsed_spec["term"]["lhs"]
actual_term = actual_closures[0]
matches = spec_term == actual_term

print(f"spec_closure_character_count={len(spec_closure_text)}")
print(f"loaded_closure_count={len(actual_closures)}")
print(f"constructor_terms_equal={matches}")
if not matches:
    print("SPEC_TERM=" + json.dumps(spec_term, sort_keys=True))
    print("ACTUAL_TERM=" + json.dumps(actual_term, sort_keys=True))
    raise SystemExit(1)
print("RESULT=PASS")
