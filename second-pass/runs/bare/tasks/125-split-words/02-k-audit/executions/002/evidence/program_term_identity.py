#!/usr/bin/env python3
"""Mechanically compare submitted solution.mpy with the solutionAST rule RHS."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
RHS = Path("/tmp/audit-work/solutionAST-rhs.mpy")
ACTUAL_JSON = Path("/tmp/audit-work/solution-actual.kast.json")
RHS_JSON = Path("/tmp/audit-work/solutionAST-rhs.kast.json")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_to_json(source: Path, destination: Path) -> subprocess.CompletedProcess:
    command = [
        "kast",
        str(source),
        "--definition",
        str(WORK / "proof-kompiled"),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
        "--output-file",
        str(destination),
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="")
    print(f"EXIT_STATUS: {completed.returncode}")
    return completed


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/program_term_identity.py")
    verification = (WORK / "verification.k").read_text()
    marker = "rule solutionAST =>"
    start = verification.index(marker) + len(marker)
    end = verification.index(
        "\n\n  // The mathematical value required by the third branch", start
    )
    rhs_text = verification[start:end].strip() + "\n"
    # K-rule syntax names empty list units explicitly; program syntax renders
    # the same units as empty argument/list positions.
    rhs_text = rhs_text.replace(".Exprs", "").replace(".Stmts", "")
    RHS.write_text(rhs_text)
    print(
        "EXTRACTED: verification.k solutionAST rule RHS -> "
        "/tmp/audit-work/solutionAST-rhs.mpy"
    )

    actual_result = parse_to_json(WORK / "solution.mpy", ACTUAL_JSON)
    rhs_result = parse_to_json(RHS, RHS_JSON)
    if actual_result.returncode != 0 or rhs_result.returncode != 0:
        raise SystemExit(1)
    actual = ACTUAL_JSON.read_bytes()
    rhs = RHS_JSON.read_bytes()
    print(f"ACTUAL_KAST_SHA256: {digest(actual)}")
    print(f"RULE_RHS_KAST_SHA256: {digest(rhs)}")
    print(f"CONSTRUCTOR_TERMS_BYTE_IDENTICAL: {actual == rhs}")
    raise SystemExit(0 if actual == rhs else 1)


if __name__ == "__main__":
    main()
