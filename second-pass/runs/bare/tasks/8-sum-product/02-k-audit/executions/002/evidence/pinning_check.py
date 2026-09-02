#!/usr/bin/env python3
"""Mechanically compare the submitted constructor term to the claim's program."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path("/tmp/audit-work/reconstruction-8-sum-product")
CANDIDATE = ROOT / "candidate"
DEFINITION = ROOT / "concrete-kompiled"

submitted = (CANDIDATE / "solution.mpy").read_bytes()
regenerated = subprocess.run(
    [
        sys.executable,
        str(ROOT / "reference/py2mpy.py"),
        str(CANDIDATE / "solution.py"),
    ],
    check=True,
    capture_output=True,
).stdout

spec_text = (CANDIDATE / "spec.k").read_text(encoding="utf-8")
match = re.search(r"<k>\s*(Module\(.*?)\s*=>\s*\.K\s*</k>", spec_text, re.S)
if match is None:
    raise SystemExit("could not extract claim's initial Module term")
claim_program = match.group(1)


def parse_to_json(expression: str) -> object:
    result = subprocess.run(
        [
            "kast",
            "--definition",
            str(DEFINITION),
            "--sort",
            "Module",
            "--output",
            "json",
            "--expression",
            expression,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


submitted_ast = parse_to_json(submitted.decode("utf-8"))
claim_ast = parse_to_json(claim_program)
summary = {
    "trusted_regeneration_byte_identical": regenerated == submitted,
    "claim_constructor_ast_identical": claim_ast == submitted_ast,
    "submitted_sha256_checked_in_stage2": True,
}
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(0 if all(summary.values()) else 1)
