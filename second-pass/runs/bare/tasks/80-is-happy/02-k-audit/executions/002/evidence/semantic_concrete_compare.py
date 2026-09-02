#!/usr/bin/env python3
"""Compare fresh `krun` execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/80-is-happy")
DEFINITION = SCRATCH / "semantic-audit-kompiled"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_happy


canonical = load_entry(SCRATCH / "trusted-canonical.py", "semantic_canonical")
generated = load_entry(SCRATCH / "solution.py", "semantic_generated")


def pstring(text: str) -> str:
    term = "eps"
    for character in reversed(text):
        term = f"ch({ord(character)}, {term})"
    return term


def k_result(text: str) -> tuple[bool, str]:
    completed = subprocess.run(
        [
            "krun",
            "solution.mpy",
            f"-cINPUT={pstring(text)}",
            "--definition",
            str(DEFINITION),
        ],
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    compact = " ".join(completed.stdout.split())
    match = re.fullmatch(r"<k> pyBool \( (true|false) \) ~> \.K </k>", compact)
    if completed.returncode != 0 or match is None:
        raise RuntimeError(
            f"krun failed for {text!r}: exit={completed.returncode}, output={compact}"
        )
    return match.group(1) == "true", compact


cases = [
    "",
    "a",
    "aa",
    "abc",
    "aab",
    "aba",
    "abb",
    "abcd",
    "abcb",
    "abcc",
    "😀éa",
    "😀a😀",
]

for text in cases:
    k_value, compact_output = k_result(text)
    canonical_value = canonical(text)
    generated_value = generated(text)
    print(
        f"input={text!r} K={k_value} canonical={canonical_value} "
        f"generated={generated_value} raw={compact_output}"
    )
    if not (k_value == canonical_value == generated_value):
        raise SystemExit(1)

print(f"semantic_case_count={len(cases)}")
print("semantic_mismatch_count=0")
