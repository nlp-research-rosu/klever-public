#!/usr/bin/env python3
"""Ground witnesses for the entry precondition and claimed summary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical"
)
candidate = load_entry(Path("/tmp/audit-work/proof/solution.py"), "witness_candidate")


def k_summary(text: str) -> tuple[bool, int, bool]:
    """Mirror only the transparent equations in verification.k."""
    codes = tuple(ord(char) for char in text)
    bracket_chars = all(code in (60, 62) for code in codes)
    balance = 0
    prefix_ok = True
    for code in codes:
        balance += 1 if code == 60 else -1
        prefix_ok = prefix_ok and balance >= 0
    bracket_correct = prefix_ok and balance == 0
    return bracket_chars, balance, bracket_correct


witnesses = ("", "<", ">", "<>", "><<>", "<<><>>", "<><>", "<<")
mismatches = 0
for text in witnesses:
    domain, delta, summary = k_summary(text)
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    print(
        f"text={text!r} codes={tuple(map(ord, text))} "
        f"bracketChars={domain} delta={delta} bracketCorrect={summary} "
        f"canonical={canonical_result} candidate={candidate_result}"
    )
    if not domain or summary != canonical_result or summary != candidate_result:
        mismatches += 1

print(f"witness_count={len(witnesses)} mismatches={mismatches}")
sys.exit(1 if mismatches else 0)
