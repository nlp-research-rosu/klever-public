#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the primeFibProgram rule RHS."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/39-prime-fib/src")
VERIFICATION = ROOT / "verification.k"
SOLUTION = ROOT / "solution.mpy"
EXTRACTED = ROOT / "audit-claim-program.mpy"
DEFINITION = ROOT / "audit-semantic-llvm-kompiled"


def parse(path: Path) -> bytes:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--sort",
        "Pgm",
        "--input",
        "program",
        "--output",
        "kast",
    ]
    print(f"KAST_COMMAND: {' '.join(command)}")
    result = subprocess.run(command, check=False, capture_output=True)
    print(f"KAST_EXIT {path.name}: {result.returncode}")
    if result.stderr:
        print(result.stderr.decode(errors="replace"))
    if result.returncode != 0:
        raise AssertionError((path, result.returncode))
    return result.stdout


def main() -> None:
    text = VERIFICATION.read_text()
    match = re.search(
        r"rule\s+primeFibProgram\s*=>\s*(.*?)\s*"
        r"\[priority\(30\)\]",
        text,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("primeFibProgram rule not found")
    rule_rhs = match.group(1).rstrip()
    empty_list_count = rule_rhs.count(".Stmts")
    external_program_rhs = rule_rhs.replace(".Stmts", "")
    EXTRACTED.write_text(external_program_rhs + "\n")
    print(
        "NORMALIZATION internal .Stmts to external empty-list spelling: "
        f"{empty_list_count} replacements"
    )

    translated = parse(SOLUTION)
    claim_term = parse(EXTRACTED)
    translated_hash = hashlib.sha256(translated).hexdigest()
    claim_hash = hashlib.sha256(claim_term).hexdigest()
    print(f"SOLUTION_KAST_SHA256 {translated_hash}")
    print(f"CLAIM_KAST_SHA256 {claim_hash}")
    print(f"BYTE_IDENTICAL_KAST {translated == claim_term}")
    if translated != claim_term:
        print("--- SOLUTION KAST ---")
        print(translated.decode(errors="replace"))
        print("--- CLAIM KAST ---")
        print(claim_term.decode(errors="replace"))
    assert translated == claim_term


if __name__ == "__main__":
    main()
