#!/usr/bin/env python3
"""Compare the submitted constructor program with the entry-claim program term."""

from __future__ import annotations

import hashlib
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/36-fizz-buzz-audit-002/candidate")
SPEC = WORK / "spec.k"
SUBMITTED = WORK / "solution.mpy"
EXTRACTED = WORK / "entry-program-from-spec.mpy"
SUBMITTED_KORE = WORK / "submitted-expanded.kore"
CLAIM_KORE = WORK / "entry-claim-expanded.kore"

text = SPEC.read_text()
entry = text.index("  claim <fizz>")
k_start = text.index("          <k>\n", entry) + len("          <k>\n")
k_end = text.index("            => .K\n", k_start)
lines = text[k_start:k_end].splitlines()
prefix = "            "
assert all(line.startswith(prefix) for line in lines)
program_text = "\n".join(line[len(prefix) :] for line in lines) + "\n"
EXTRACTED.write_text(program_text)


def run_kast(source: Path, destination: Path) -> None:
    command = [
        "kast",
        str(source),
        "--definition",
        str(WORK / "proof-kompiled"),
        "--module",
        "VERIFICATION",
        "--sort",
        "Program",
        "--expand-macros",
        "--output",
        "kore",
        "--output-file",
        str(destination),
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(command, cwd=WORK)
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


run_kast(SUBMITTED, SUBMITTED_KORE)
run_kast(EXTRACTED, CLAIM_KORE)

submitted_bytes = SUBMITTED_KORE.read_bytes()
claim_bytes = CLAIM_KORE.read_bytes()
submitted_hash = hashlib.sha256(submitted_bytes).hexdigest()
claim_hash = hashlib.sha256(claim_bytes).hexdigest()
print(f"submitted_expanded_sha256={submitted_hash}")
print(f"entry_claim_expanded_sha256={claim_hash}")
print(f"expanded_byte_identity={submitted_bytes == claim_bytes}")
if submitted_bytes != claim_bytes:
    raise SystemExit(1)
