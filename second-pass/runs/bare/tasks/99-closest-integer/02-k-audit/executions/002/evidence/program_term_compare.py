#!/usr/bin/env python3
"""Mechanical constructor-level comparison of source and proof program terms."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


work = Path("/tmp/audit-work/candidate")
source = (work / "solution.regenerated.mpy").read_text().strip()

verification = (work / "verification.k").read_text()
marker = "rule solutionProgram =>"
start = verification.index(marker) + len(marker)
end = verification.index("\n\n  // Mathematical reference", start)
proof_term = verification[start:end].strip()
assert proof_term.count(".Stmts") == 1
proof_normalized = proof_term.replace(".Stmts", "", 1)

source_path = work / "source-for-compare.mpy"
proof_path = work / "proof-program-for-compare.mpy"
source_path.write_text(source + "\n")
proof_path.write_text(proof_normalized + "\n")


def kast(path: Path):
    command = [
        "kast",
        str(path),
        "--definition",
        str(work / "semantic-audit-kompiled"),
        "--sort",
        "Program",
        "--output",
        "json",
    ]
    run = subprocess.run(command, cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"COMMAND {command!r}")
    print(f"EXIT {run.returncode}")
    if run.stderr:
        print(f"STDERR {run.stderr}")
    assert run.returncode == 0
    return json.loads(run.stdout)


source_kast = kast(source_path)
proof_kast = kast(proof_path)
source_json = json.dumps(source_kast, sort_keys=True, separators=(",", ":"))
proof_json = json.dumps(proof_kast, sort_keys=True, separators=(",", ":"))
source_hash = hashlib.sha256(source_json.encode()).hexdigest()
proof_hash = hashlib.sha256(proof_json.encode()).hexdigest()

print("SOURCE_NORMALIZED")
print(source)
print("PROOF_TERM")
print(proof_term)
print("PROOF_NORMALIZED_FOR_PROGRAM_PARSER")
print(proof_normalized)
print(f"SOURCE_KAST_SHA256 {source_hash}")
print(f"PROOF_KAST_SHA256 {proof_hash}")
print(f"KAST_EQUAL {source_kast == proof_kast}")
assert source_kast == proof_kast
