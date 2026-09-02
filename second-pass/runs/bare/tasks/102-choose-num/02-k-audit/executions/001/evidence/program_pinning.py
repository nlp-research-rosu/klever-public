#!/usr/bin/env python3
"""Extract chooseNumProgram's constructor RHS and compare it with solution.mpy."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def balanced_constructor(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise RuntimeError("unterminated constructor")


verification = Path("/tmp/audit-work/verification.k").read_text(encoding="utf-8")
submitted = Path("/tmp/audit-work/solution.mpy").read_text(encoding="utf-8").strip()
rule_start = verification.index("rule chooseNumProgram")
rhs_start = verification.index("Module(", rule_start)
extracted = balanced_constructor(verification, rhs_start)

artifact = Path("/audit-output/evidence/extracted-chooseNumProgram.mpy")
artifact.write_text(extracted + "\n", encoding="utf-8")

normalize = lambda value: re.sub(r"\s+", "", value)
submitted_normalized = normalize(submitted)
extracted_normalized = normalize(extracted)
print(f"submitted_normalized_sha256={hashlib.sha256(submitted_normalized.encode()).hexdigest()}")
print(f"extracted_normalized_sha256={hashlib.sha256(extracted_normalized.encode()).hexdigest()}")
print(f"constructor_token_identity={submitted_normalized == extracted_normalized}")
print(f"extracted_artifact={artifact}")
if submitted_normalized != extracted_normalized:
    raise SystemExit(1)
