#!/usr/bin/env python3
"""Mechanically compare the claim's solutionProgram RHS with solution.mpy."""

from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate-src")
DEFINITION = Path("/tmp/audit-work/build-proof/verification-kompiled")
EVIDENCE = Path("/audit-output/evidence")


def run_kast(path: Path, output: Path) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "MINPATH-VERIFICATION",
        "--sort",
        "Program",
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command,
        cwd=SOURCE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=120,
    )
    output.write_text(completed.stdout)
    print(f"command={shlex.join(command)}")
    print(f"exit_status={completed.returncode}")
    if completed.stderr:
        print("stderr=" + completed.stderr)
    assert completed.returncode == 0
    return json.loads(completed.stdout)


def main() -> None:
    verification = (SOURCE / "verification.k").read_text()
    marker = "  rule solutionProgram =>\n"
    assert verification.count(marker) == 1
    rhs = verification.split(marker, 1)[1].rsplit("\nendmodule", 1)[0].strip()
    # `.Stmts` and `.Exprs` are K rule-language spellings for generated empty
    # list units. The concrete Program parser spells the same units as empty
    # argument/list positions, as emitted by the trusted translator.
    rhs = rhs.replace(".Stmts", "").replace(".Exprs", "")
    rhs_path = Path("/tmp/audit-work/solution-program-rhs.mpy")
    rhs_path.write_text(rhs + "\n")

    submitted_json_path = EVIDENCE / "04_solution_mpy.kast.json"
    rhs_json_path = EVIDENCE / "04_solution_program_rhs.kast.json"
    submitted = run_kast(SOURCE / "solution.mpy", submitted_json_path)
    rhs_term = run_kast(rhs_path, rhs_json_path)
    submitted_bytes = json.dumps(
        submitted, sort_keys=True, separators=(",", ":")
    ).encode()
    rhs_bytes = json.dumps(rhs_term, sort_keys=True, separators=(",", ":")).encode()
    print(f"submitted_kast_sha256={hashlib.sha256(submitted_bytes).hexdigest()}")
    print(f"rhs_kast_sha256={hashlib.sha256(rhs_bytes).hexdigest()}")
    print(f"constructor_ast_equal={submitted == rhs_term}")
    assert submitted == rhs_term
    print("REAL_PROGRAM_CONSTRUCTOR_PINNING_OK")


if __name__ == "__main__":
    main()
