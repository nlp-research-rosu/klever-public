#!/usr/bin/env python3
"""Mechanically compare the submitted constructor term with the spec term."""

from pathlib import Path


def balanced_module_term(text: str) -> str:
    start = text.find("Module(")
    if start < 0:
        raise ValueError("Module( term not found")
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced Module term")


root = Path("/tmp/audit-work/candidate-src")
submitted = balanced_module_term((root / "solution.mpy").read_text())
claimed = balanced_module_term((root / "spec.k").read_text())
submitted_normalized = "".join(submitted.split())
claimed_normalized = "".join(claimed.split())

print(f"submitted_chars={len(submitted)} normalized={len(submitted_normalized)}")
print(f"claimed_chars={len(claimed)} normalized={len(claimed_normalized)}")
print(f"normalized_terms_equal={submitted_normalized == claimed_normalized}")
print(f"submitted_sha256_input={submitted_normalized}")
raise SystemExit(0 if submitted_normalized == claimed_normalized else 1)
