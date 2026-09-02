#!/usr/bin/env python3
"""Mechanically compare the submitted program term with the entry-claim term."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/reconstruction")


def balanced_term(text: str, marker: str) -> str:
    marker_at = text.index(marker)
    start = text.index("Module(", marker_at)
    depth = 0
    quote = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unterminated Module term in spec.k")


def normalized_kore(path: Path) -> bytes:
    command = [
        "kast",
        str(path),
        "--definition",
        str(ROOT / "verification-audit-kompiled"),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "kore",
    ]
    result = subprocess.run(command, check=False, capture_output=True)
    if result.stderr:
        sys.stderr.buffer.write(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"kast failed with exit {result.returncode}: {path}")
    return result.stdout


def main() -> int:
    spec_text = (ROOT / "spec.k").read_text()
    entry_term_raw = balanced_term(spec_text, "claim [vowels-count]")
    # In rule syntax the list terminator is written explicitly as `.Stmts`.
    # The MPY program parser inserts that terminator through List{Stmt, ""},
    # so remove only those standalone terminator tokens before parsing both
    # sides to the same KORE constructor representation.
    entry_term = re.sub(r"(?m)^\s*\.Stmts(?=\))", "", entry_term_raw)
    extracted = ROOT / "entry-claimed-program.mpy"
    extracted.write_text(entry_term + "\n")
    (ROOT / "entry-claimed-program.raw.txt").write_text(entry_term_raw + "\n")

    submitted_kore = normalized_kore(ROOT / "solution.mpy")
    claimed_kore = normalized_kore(extracted)
    (ROOT / "solution.normalized.kore").write_bytes(submitted_kore)
    (ROOT / "entry-claimed-program.normalized.kore").write_bytes(claimed_kore)

    equal = submitted_kore == claimed_kore
    print("submitted_source=", ROOT / "solution.mpy", sep="")
    print("extracted_entry_term=", extracted, sep="")
    print("submitted_normalized_bytes=", len(submitted_kore), sep="")
    print("claimed_normalized_bytes=", len(claimed_kore), sep="")
    print("normalization=removed explicit rule-syntax .Stmts list terminators")
    print("constructor_level_identity=", equal, sep="")
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
