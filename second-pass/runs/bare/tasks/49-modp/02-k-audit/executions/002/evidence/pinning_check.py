#!/usr/bin/env python3
"""Mechanically compare the first entry claim's program term with solution.mpy."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
spec_text = (ROOT / "spec.k").read_text()
match = re.search(r"claim\s+<k>\s*(.*?)\s*=>\s*\.K\s*</k>", spec_text, re.DOTALL)
if match is None:
    raise RuntimeError("could not extract first entry claim's <k> LHS")
claim_program = match.group(1)

file_command = [
    "kast",
    "--definition",
    "semantic-llvm-kompiled",
    "--input",
    "program",
    "--output",
    "json",
    "solution.mpy",
]
claim_command = [
    "kast",
    "--definition",
    "semantic-llvm-kompiled",
    "--input",
    "program",
    "--output",
    "json",
    "--expression",
    claim_program,
]

print("COMMAND[file]:", " ".join(file_command))
file_run = subprocess.run(file_command, cwd=ROOT, text=True, capture_output=True)
print("EXIT[file]:", file_run.returncode)
if file_run.stderr:
    print(file_run.stderr)
print("COMMAND[claim]: kast --definition semantic-llvm-kompiled "
      "--input program --output json --expression '<extracted first claim LHS>'")
claim_run = subprocess.run(claim_command, cwd=ROOT, text=True, capture_output=True)
print("EXIT[claim]:", claim_run.returncode)
if claim_run.stderr:
    print(claim_run.stderr)
if file_run.returncode != 0 or claim_run.returncode != 0:
    sys.exit(2)

file_term = json.loads(file_run.stdout)
claim_term = json.loads(claim_run.stdout)
file_canonical = json.dumps(file_term, sort_keys=True, separators=(",", ":")).encode()
claim_canonical = json.dumps(claim_term, sort_keys=True, separators=(",", ":")).encode()
print("solution_kast_sha256:", hashlib.sha256(file_canonical).hexdigest())
print("claim_kast_sha256:", hashlib.sha256(claim_canonical).hexdigest())
print("constructor_terms_equal:", file_term == claim_term)
print("extracted_claim_program:", " ".join(claim_program.split()))
sys.exit(0 if file_term == claim_term else 1)
