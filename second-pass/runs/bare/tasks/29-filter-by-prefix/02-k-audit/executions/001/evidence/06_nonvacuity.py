#!/usr/bin/env python3
"""Require the reviewer-authored false result mutation to parse and get stuck."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


source = Path("/audit-output/evidence/06_spec_vacuity.k")
scratch = Path("/tmp/audit-work/candidate/spec-vacuity.k")
if source.read_bytes() != scratch.read_bytes():
    raise SystemExit("scratch mutation does not match preserved evidence mutation")

base = [
    "kprove",
    "spec-vacuity.k",
    "--definition",
    "/tmp/audit-work/proof-kompiled",
    "--spec-module",
    "SPEC-VACUITY",
    "--trusted",
    "loop-correct-vacuity-support",
]

dry_command = base + ["--dry-run"]
print(f"COMMAND: {shlex.join(dry_command)}")
dry = subprocess.run(
    dry_command,
    cwd="/tmp/audit-work/candidate",
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
print(dry.stdout.rstrip())
print(f"EXIT: {dry.returncode}")
print()

print(f"COMMAND: {shlex.join(base)}")
proof = subprocess.run(
    base,
    cwd="/tmp/audit-work/candidate",
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
print(proof.stdout.rstrip())
print(f"EXIT: {proof.returncode}")
print()

has_stuck = "WarnStuckClaimState" in proof.stdout
has_mutated_obligation = (
    "__AUDIT_FALSE__" in proof.stdout
    or "appendOne" in proof.stdout
    or "LblappendOne" in proof.stdout
)
print("SATISFYING_WITNESS:")
print('  INPUT = nil, PREFIX = "a", initial env/functions = .Map, output = noOutput')
print("  concrete actual output = listVal(nil)")
print('  mutated required output = listVal(cons("__AUDIT_FALSE__", nil))')
print(f"dry_run_success={dry.returncode == 0}")
print(f"proof_rejected={proof.returncode != 0}")
print(f"stuck_claim_residual={has_stuck}")
print(f"residual_mentions_mutated_obligation={has_mutated_obligation}")

ok = (
    dry.returncode == 0
    and proof.returncode != 0
    and has_stuck
    and has_mutated_obligation
)
raise SystemExit(0 if ok else 1)
