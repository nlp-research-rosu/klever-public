#!/usr/bin/env python3
"""Mutate the actual encoded loop body and require the original proof to fail."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


preserved = Path("/audit-output/evidence/04_verification_body_mutant.k")
scratch = Path("/tmp/audit-work/body-mutant/verification.k")
if preserved.read_bytes() != scratch.read_bytes():
    raise SystemExit("scratch body mutant differs from preserved evidence")


def run(command: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout.rstrip())
    print(f"EXIT: {completed.returncode}")
    print()
    return completed


build = run(
    [
        "kompile",
        "--backend",
        "haskell",
        "semantic.k",
        "--main-module",
        "SEMANTIC",
        "--syntax-module",
        "VERIFICATION",
        "--output-definition",
        "/tmp/audit-work/body-mutant-kompiled",
    ],
    "/tmp/audit-work/body-mutant",
)
if build.returncode != 0:
    raise SystemExit(1)

proof = run(
    [
        "kprove",
        "spec.k",
        "--definition",
        "/tmp/audit-work/body-mutant-kompiled",
        "--spec-module",
        "SPEC",
    ],
    "/tmp/audit-work/body-mutant",
)

print("MUTATION: loop body appends every string and omits startswith/If")
print('FALSE_WITNESS: strings=["b"], prefix="a"; mutant returns ["b"], spec requires []')
print(f"proof_rejected={proof.returncode != 0}")
print(f"stuck_claim_residual={'WarnStuckClaimState' in proof.stdout}")
ok = proof.returncode != 0 and "WarnStuckClaimState" in proof.stdout
raise SystemExit(0 if ok else 1)
