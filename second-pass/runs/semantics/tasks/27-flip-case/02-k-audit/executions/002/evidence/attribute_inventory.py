#!/usr/bin/env python3
"""Summarize K attributes across the complete audited source set."""

from pathlib import Path
import re

root = Path("/reference/reference-semantics")
files = [root / "semantics.k", *sorted((root / "semantics").glob("*.k"))]
files += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
patterns = {
    "priority_rules": r"\[priority\(",
    "owise_rules": r"\[owise\]",
    "concrete_rules": r"\[concrete\]",
    "no_evaluators_declarations": r"^\s*syntax .*no-evaluators",
    "symbol_declarations": r"^\s*syntax .*symbol\(",
    "simplification_or_functional": r"^\s*(?:rule|claim|syntax).*(?:simplification|simplifier|functional)",
}
texts = {path: path.read_text().splitlines() for path in files}
for label, pattern in patterns.items():
    matches = [
        (path, lineno, line.strip())
        for path, lines in texts.items()
        for lineno, line in enumerate(lines, 1)
        if re.search(pattern, line)
    ]
    print(f"{label}={len(matches)}")
    if label == "symbol_declarations":
        for path, lineno, line in matches:
            print(f"  {path}:{lineno}: {line}")
