#!/usr/bin/env python3
"""Check that spec.k embeds the exact translated solution.mpy module term."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent


def compact(text):
    return "".join(text.split())


solution_term = compact((ROOT / "solution.mpy").read_text(encoding="utf-8"))
spec_text = compact((ROOT / "spec.k").read_text(encoding="utf-8"))

if solution_term not in spec_text:
    raise SystemExit("IDENTITY_CHECK_FAILED: solution.mpy is not embedded in spec.k")

print("IDENTITY_CHECK_PASSED: exact whitespace-normalized solution.mpy term found in spec.k")
