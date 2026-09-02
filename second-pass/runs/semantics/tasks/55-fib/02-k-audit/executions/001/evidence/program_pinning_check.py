#!/usr/bin/env python3
"""Check that verification.k's nullary program definitions expand to solution.mpy."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/55-fib-audit")
verification = (ROOT / "candidate-src/verification.k").read_text()
submitted = (ROOT / "candidate-src/solution.mpy").read_text()


def rule_rhs(start: str, end: str) -> str:
    pattern = rf"rule\s+{re.escape(start)}\s*=>\s*(.*?)\n\s*rule\s+{re.escape(end)}\s*=>"
    match = re.search(pattern, verification, re.DOTALL)
    if match is None:
        raise AssertionError(f"could not extract {start}")
    return match.group(1).strip()


fib_body = rule_rhs("fibBody", "fibClosure")
fib_closure = rule_rhs("fibClosure", "fibProgram")
program_match = re.search(
    r"rule\s+fibProgram\s*=>\s*(.*?)\n\s*\n\s*// A mathematical",
    verification,
    re.DOTALL,
)
if program_match is None:
    raise AssertionError("could not extract fibProgram")
fib_program = program_match.group(1).strip()


def compact(text: str) -> str:
    out = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    if quoted:
        raise AssertionError("unterminated quoted string while normalizing")
    return "".join(out)


expanded = fib_program.replace("fibBody", fib_body)
print(f"FIB_BODY={fib_body}")
print(f"FIB_CLOSURE={fib_closure}")
print(f"FIB_PROGRAM={fib_program}")
print(f"EXPANDED_PROGRAM={expanded}")
print(f"SUBMITTED_PROGRAM={submitted.strip()}")
print(f"NORMALIZED_EXPANDED={compact(expanded)}")
print(f"NORMALIZED_SUBMITTED={compact(submitted)}")
print(f"PROGRAM_TERM_IDENTICAL={compact(expanded) == compact(submitted)}")
if compact(expanded) != compact(submitted):
    raise SystemExit(1)


def load_fib(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib


canonical = load_fib("pinning_canonical", ROOT / "trusted/canonical.py")
candidate = load_fib("pinning_candidate", ROOT / "candidate-src/solution.py")


def fib_run(a: int, b: int, i: int, n: int) -> int:
    while i < n:
        a, b, i = b, a + b, i + 1
    return a


for n in [0, 1, 2, 3, 10]:
    formal = fib_run(0, 1, 0, n)
    trusted_python = canonical(n)
    submitted_python = candidate(n)
    print(
        f"ENTRY_WITNESS N={n} fibSpec={formal} "
        f"canonical={trusted_python} candidate={submitted_python}"
    )
    assert formal == trusted_python == submitted_python

print(
    "LOOP_WITNESS "
    "I=0 N=3 A=0 B=1 OLD_INDEX=0 L=1 CONT=Return(Name(\"a\")); "
    f"destination_a={fib_run(0, 1, 0, 3)}"
)
