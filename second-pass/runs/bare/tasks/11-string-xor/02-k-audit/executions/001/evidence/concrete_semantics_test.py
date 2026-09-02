#!/usr/bin/env python3
"""Compare freshly compiled generated K semantics with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
from pathlib import Path


SOURCE = Path("/tmp/audit-work/11-string-xor-audit/source")
DEFINITION = Path("/tmp/audit-work/11-string-xor-audit/semantic-llvm-kompiled")
CASES_PATH = Path("/audit-output/evidence/concrete-semantics-inputs.json")


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load_entry(Path("/reference/canonical.py"), "concrete_canonical")
candidate = load_entry(SOURCE / "solution.py", "concrete_candidate")

cases = [
    {"name": "prompt-example", "a": "010", "b": "110"},
    {"name": "both-empty", "a": "", "b": ""},
    {"name": "left-empty", "a": "", "b": "101"},
    {"name": "right-empty", "a": "101", "b": ""},
    {"name": "equal-first-bit", "a": "00", "b": "01"},
    {"name": "different-first-bit", "a": "10", "b": "00"},
    {"name": "left-shorter", "a": "0101", "b": "11"},
    {"name": "right-shorter", "a": "11", "b": "0101"},
    {"name": "all-bit-branches", "a": "0011", "b": "0101"},
    {"name": "representative-longer", "a": "011010011001", "b": "110010101101"},
]
CASES_PATH.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")


def text_term(bits: str) -> str:
    term = "empty"
    for bit in reversed(bits):
        term = f"cons({'true' if bit == '1' else 'false'},{term})"
    return term


def segment_term(bits: str) -> str:
    encoded = sum((bit == "1") << index for index, bit in enumerate(bits))
    return f"segment({len(bits)},seed({encoded}))"


failures = 0
for case in cases:
    left = case["a"]
    right = case["b"]
    expected = canonical(left, right)
    python_actual = candidate(left, right)
    python_matches = python_actual == expected
    for encoding, constructor in (
        ("concrete-cons", text_term),
        ("claim-segment-seed", segment_term),
    ):
        args = f"Args(str({constructor(left)}),str({constructor(right)}))"
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f"-cARGS={args}",
            "--output",
            "pretty",
        ]
        print("COMMAND: " + shlex.join(command))
        result = subprocess.run(
            command,
            cwd=SOURCE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        normalized = "".join(result.stdout.split())
        expected_fragment = f"returned(str({text_term(expected)}))~>.K"
        k_matches = result.returncode == 0 and expected_fragment in normalized
        print(
            json.dumps(
                {
                    "name": case["name"],
                    "encoding": encoding,
                    "a": left,
                    "b": right,
                    "expected": expected,
                    "candidate_python": python_actual,
                    "python_matches": python_matches,
                    "krun_exit": result.returncode,
                    "k_matches": k_matches,
                },
                sort_keys=True,
            )
        )
        if not k_matches:
            print("KRUN_OUTPUT_BEGIN")
            print(result.stdout.rstrip())
            print("KRUN_OUTPUT_END")
        if not (python_matches and k_matches):
            failures += 1

print(
    json.dumps(
        {"source_cases": len(cases), "k_executions": 2 * len(cases), "failures": failures},
        sort_keys=True,
    )
)
raise SystemExit(1 if failures else 0)
