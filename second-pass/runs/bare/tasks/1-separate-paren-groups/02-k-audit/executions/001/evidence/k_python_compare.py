#!/usr/bin/env python3
"""Run the fresh LLVM semantics and compare its result with both Python files."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
DEFINITION = WORK / "semantic-llvm-kompiled"


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


canonical = load_entry(
    "concrete_trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
submitted = load_entry("concrete_submitted", WORK / "solution.py")


def parse_k_result(stdout: str):
    match = re.search(r"<result>\s*(.*?)\s*</result>", stdout, re.DOTALL)
    if not match:
        raise AssertionError(f"missing <result> cell:\n{stdout}")
    term = " ".join(match.group(1).split())
    if term == "OutList ( .Outputs )":
        return [], term
    if not term.startswith("OutList ("):
        raise AssertionError(f"unexpected result term: {term}")
    groups = []
    for body in re.findall(r"out \( (.*?) \.Chars \)", term):
        chars = re.findall(r"\b(?:LP|RP|SP)\b", body)
        groups.append(
            "".join({"LP": "(", "RP": ")", "SP": " "}[char] for char in chars)
        )
    return groups, term


intended_cases = [
    ("documented", "( ) (( )) (( )( ))"),
    ("empty", ""),
    ("spaces-only", "     "),
    ("single", "()"),
    ("nested", "(((())))"),
    ("adjacent", "()(())(()())"),
    ("space-boundaries", "  ( ( ) )  ( ) "),
]

for label, source in intended_cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f'-cINPUT=Raw("{source}")',
        "--output",
        "pretty",
    ]
    print(f"\nCASE={label} SOURCE={source!r}")
    print("$", shlex.join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print(f"[exit {completed.returncode}]")
    if completed.stderr:
        print("STDERR:", completed.stderr)
    assert completed.returncode == 0
    k_value, result_term = parse_k_result(completed.stdout)
    canonical_value = canonical(source)
    submitted_value = submitted(source)
    print("K_RESULT_TERM:", result_term)
    print("K_PARSED:", k_value)
    print("CANONICAL_PYTHON:", canonical_value)
    print("SUBMITTED_PYTHON:", submitted_value)
    assert k_value == canonical_value == submitted_value

# Diagnostic for the proof claim's broader Encoded alphabet. This input is
# deliberately outside the prompt's balanced-groups precondition.
source = ")"
command = [
    "krun",
    "solution.mpy",
    "--definition",
    str(DEFINITION),
    f'-cINPUT=Raw("{source}")',
    "--output",
    "pretty",
]
print(f"\nOUTSIDE_INTENDED_DOMAIN_DIAGNOSTIC SOURCE={source!r}")
print("$", shlex.join(command))
completed = subprocess.run(
    command,
    cwd=WORK,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)
print(f"[exit {completed.returncode}]")
assert completed.returncode == 0
k_value, result_term = parse_k_result(completed.stdout)
print("K_RESULT_TERM:", result_term)
print("K_PARSED:", k_value)
print("CANONICAL_PYTHON:", canonical(source))
print("SUBMITTED_PYTHON:", submitted(source))
assert k_value == [")"]
assert canonical(source) == submitted(source) == []

print("\nINTENDED_K_PYTHON_COMPARISONS=7")
print("INTENDED_MISMATCHES=0")
print("OUTSIDE_DOMAIN_SEMANTIC_DIVERGENCE=1")
