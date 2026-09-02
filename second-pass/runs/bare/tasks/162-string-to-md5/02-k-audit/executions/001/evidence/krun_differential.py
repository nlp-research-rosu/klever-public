#!/usr/bin/env python3
"""Compare freshly rebuilt generated K semantics with Python execution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable


ROOT = Path("/tmp/audit-work/reconstruction")
DEFINITION = ROOT / "semantic-haskell-audit-kompiled"


def load_entry(module_name: str, path: Path) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_to_md5


def python_outcome(function: Callable[[str], Any], value: str) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value)}
    except BaseException as error:
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


def parse_k_result(output: str) -> dict[str, Any]:
    match = re.search(r"<result>\s*(.*?)\s*</result>", output, re.DOTALL)
    if match is None:
        return {"kind": "unparsed", "result_cell": None}
    result_cell = match.group(1).strip()
    if result_cell == "pyNone":
        return {"kind": "return", "value": None}
    string_match = re.fullmatch(
        r'pyString\s*\(\s*"([0-9a-f]{32})"\s*\)', result_cell
    )
    if string_match is not None:
        return {"kind": "return", "value": string_match.group(1)}
    return {"kind": "unparsed", "result_cell": result_cell}


def main() -> int:
    candidate = load_entry("candidate_for_krun", ROOT / "solution.py")
    canonical = load_entry("canonical_for_krun", ROOT / "canonical.py")
    cases = [
        ("empty-branch", ""),
        ("prompt-example", "Hello world"),
        ("padding-55", "a" * 55),
        ("padding-56", "a" * 56),
        ("block-64", "b" * 64),
        ("block-65", "b" * 65),
        ("submitted-80", "a" * 80),
        ("utf8-two-byte", "é"),
        ("utf8-three-byte", "€"),
        ("utf8-four-byte", "😀"),
    ]
    failures = 0
    for label, value in cases:
        text_term = json.dumps(value, ensure_ascii=False)
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f"-cTEXT={text_term}",
        ]
        completed = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=60
        )
        k_outcome = (
            parse_k_result(completed.stdout)
            if completed.returncode == 0
            else {
                "kind": "krun-error",
                "returncode": completed.returncode,
                "stderr": completed.stderr[-1000:],
            }
        )
        candidate_outcome = python_outcome(candidate, value)
        canonical_outcome = python_outcome(canonical, value)
        match = completed.returncode == 0 and k_outcome == candidate_outcome
        if not match:
            failures += 1
        print(
            json.dumps(
                {
                    "label": label,
                    "input": value,
                    "command": command,
                    "exit_status": completed.returncode,
                    "k": k_outcome,
                    "candidate_python": candidate_outcome,
                    "canonical_python": canonical_outcome,
                    "k_matches_candidate": match,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print(json.dumps({"summary": {"cases": len(cases), "failures": failures}}))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
