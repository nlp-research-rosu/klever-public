#!/usr/bin/env python3
"""Compare the freshly rebuilt generated K semantics with both Python programs."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/66-digitsum-audit")
DEFINITION = SCRATCH / "audit-semantic-llvm-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_entry("trusted_canonical_for_k", SCRATCH / "trusted-canonical.py")
candidate = load_entry("candidate_for_k", SCRATCH / "solution.py")

cases = [
    "",
    "@",
    "A",
    "Z",
    "[",
    "abAB",
    "abcCd",
    "helloE",
    "woArBld",
    "aAaaaXa",
    "AZaz09",
    'A"Z',
    "A\\Z",
    "A\nZ",
    "É",
    "Ω",
    "AΩZ",
    "𝔄",
]

print("COMMAND TEMPLATE: krun solution.mpy --definition audit-semantic-llvm-kompiled "
      "-cINPUT=<K-String> --output pretty")
print(f"case_count={len(cases)}")
for text in cases:
    k_literal = json.dumps(text, ensure_ascii=False)
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={k_literal}",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        print(f"K_FAILURE input={ascii(text)} exit={completed.returncode}")
        print("stdout=" + completed.stdout[-2000:])
        print("stderr=" + completed.stderr[-2000:])
        raise SystemExit(completed.returncode)
    match = re.search(r"intVal\s*\(\s*(-?\d+)\s*\)", completed.stdout)
    if match is None:
        print(f"K_RESULT_PARSE_FAILURE input={ascii(text)}")
        print(completed.stdout[-4000:])
        raise SystemExit(2)
    k_value = int(match.group(1))
    candidate_value = candidate(text)
    canonical_value = canonical(text)
    assert k_value == candidate_value
    print(
        f"input={ascii(text)} k={k_value} candidate={candidate_value} "
        f"canonical={canonical_value} "
        f"k_candidate_match=yes "
        f"k_canonical_match={'yes' if k_value == canonical_value else 'NO'}"
    )

print("K_SEMANTICS_CANDIDATE_DIFFERENTIAL=PASS")
