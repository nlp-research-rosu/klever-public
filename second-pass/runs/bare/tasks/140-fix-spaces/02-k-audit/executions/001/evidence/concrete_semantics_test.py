#!/usr/bin/env python3
"""Compare freshly rebuilt K execution with independent Python executions."""

from __future__ import annotations

import importlib.util
import ast
import json
import re
import shlex
import subprocess


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


submitted = load_entry("submitted_solution_concrete", "/tmp/audit-work/src/solution.py")
canonical = load_entry("trusted_canonical_concrete", "/reference/canonical.py")

inputs = [
    "",
    "Example",
    "Example 1",
    " Example 2",
    " Example   3",
    " ",
    "  ",
    "   ",
    "    ",
    "a ",
    "a  ",
    "a   ",
    "a b",
    "a  b",
    "a   b",
    "  a  ",
    "é  λ",
]

failures: list[dict[str, object]] = []
canonical_divergences: list[dict[str, str]] = []

for text in inputs:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "audit-semantic-kompiled",
        f"-cINPUT={json.dumps(text, ensure_ascii=False)}",
    ]
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/src",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"COMMAND: {shlex.join(command)}")
    print(f"EXIT_STATUS: {completed.returncode}")
    print(completed.stdout.rstrip())

    python_value = submitted(text)
    canonical_value = canonical(text)
    match = re.search(r'<result>\s*("(?:[^"\\]|\\.)*")\s*~>\s*\.K', completed.stdout)
    if completed.returncode == 0 and match and all(ord(char) < 128 for char in python_value):
        k_value = ast.literal_eval(match.group(1))
    elif completed.returncode == 0 and match:
        # The Haskell pretty-printer uses backend-specific \x escapes for
        # non-ASCII K strings. Compare the raw result token with the raw input
        # token produced by parsing the independently computed Python value.
        expected_command = [
            "krun",
            "solution.mpy",
            "--definition",
            "audit-semantic-kompiled",
            f"-cINPUT={json.dumps(python_value, ensure_ascii=False)}",
        ]
        expected_completed = subprocess.run(
            expected_command,
            cwd="/tmp/audit-work/src",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"EXPECTED-TOKEN COMMAND: {shlex.join(expected_command)}")
        print(f"EXPECTED-TOKEN EXIT_STATUS: {expected_completed.returncode}")
        print(expected_completed.stdout.rstrip())
        expected_match = re.search(
            r'<input>\s*("(?:[^"\\]|\\.)*")\s*</input>',
            expected_completed.stdout,
        )
        if (
            expected_completed.returncode == 0
            and expected_match
            and match.group(1) == expected_match.group(1)
        ):
            k_value = python_value
        else:
            k_value = f"K_TOKEN:{match.group(1)}"
    else:
        k_value = None
    print(
        "COMPARISON: "
        + json.dumps(
            {
                "input": text,
                "k": k_value,
                "submitted_python": python_value,
                "trusted_canonical": canonical_value,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    print()

    if completed.returncode != 0 or k_value != python_value:
        failures.append(
            {
                "input": text,
                "krun_exit": completed.returncode,
                "k": k_value,
                "submitted_python": python_value,
            }
        )
    if k_value != canonical_value:
        canonical_divergences.append(
            {
                "input": text,
                "k": str(k_value),
                "trusted_canonical": canonical_value,
            }
        )

print(
    "SUMMARY: "
    + json.dumps(
        {
            "inputs_checked": len(inputs),
            "k_vs_submitted_failures": failures,
            "k_vs_canonical_divergences": canonical_divergences,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
)
raise SystemExit(1 if failures else 0)
