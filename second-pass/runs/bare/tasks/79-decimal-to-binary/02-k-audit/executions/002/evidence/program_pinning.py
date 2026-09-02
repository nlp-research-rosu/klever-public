#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and all entry claims."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


program_path = Path(sys.argv[1])
spec_path = Path(sys.argv[2])
program = normalize(program_path.read_text())
spec = spec_path.read_text()
claim_terms = re.findall(r"<k>\s*(Module\(.*?)\s*=>\s*\.K\s*</k>", spec, re.DOTALL)

print(f"COMMAND: python3 {Path(__file__)} {program_path} {spec_path}")
print(f"PROGRAM_NORMALIZED_SHA256={hashlib.sha256(program.encode()).hexdigest()}")
print(f"ENTRY_CLAIM_COUNT={len(claim_terms)}")
failures = 0
for index, claim_term in enumerate(claim_terms, 1):
    normalized = normalize(claim_term)
    same = normalized == program
    failures += not same
    print(
        f"CLAIM_{index}_TERM_SHA256={hashlib.sha256(normalized.encode()).hexdigest()} "
        f"EQUAL={same}"
    )
print(f"MISMATCH_COUNT={failures}")
print(f"EXIT_STATUS={1 if failures else 0}")
raise SystemExit(1 if failures else 0)
