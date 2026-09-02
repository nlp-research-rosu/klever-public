#!/usr/bin/env python3
"""Mechanical source inventory supporting the manual rule audit."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


CANDIDATE = Path("/candidate")
files = [
    CANDIDATE / "solution.mpy",
    CANDIDATE / "semantic.k",
    CANDIDATE / "verification.k",
    CANDIDATE / "spec.k",
]

for path in files:
    print(
        f"FILE {path} bytes={path.stat().st_size} "
        f"sha256={hashlib.sha256(path.read_bytes()).hexdigest()}"
    )
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if (
            stripped.startswith("module ")
            or stripped.startswith("imports ")
            or stripped.startswith("syntax ")
            or stripped.startswith("configuration")
            or stripped.startswith("rule ")
            or stripped.startswith("claim ")
            or "[function" in stripped
            or "[total" in stripped
            or "[functional" in stripped
            or "[simplification" in stripped
            or "[priority" in stripped
            or "[owise" in stripped
            or "[anywhere" in stripped
        ):
            print(f"{number:04d}: {stripped}")

program = (CANDIDATE / "solution.mpy").read_text(encoding="utf-8")
spec = (CANDIDATE / "spec.k").read_text(encoding="utf-8")
verification = (CANDIDATE / "verification.k").read_text(encoding="utf-8")
semantic = (CANDIDATE / "semantic.k").read_text(encoding="utf-8")

normalize = lambda text: re.sub(r"\s+", "", text)
normalized_program = normalize(program)
claim_count = len(re.findall(r"(?m)^\s*claim\b", spec))
print(f"NORMALIZED_PROGRAM={normalized_program}")
print(
    "EXACT_PROGRAM_OCCURRENCES_IN_SPEC="
    + str(normalize(spec).count(normalized_program))
)
print(f"CLAIM_COUNT_SPEC={claim_count}")
print(
    "LOCAL_RULE_COUNT_SEMANTIC="
    + str(len(re.findall(r"(?m)^\s*rule\b", semantic)))
)
print(
    "LOCAL_RULE_COUNT_VERIFICATION="
    + str(len(re.findall(r"(?m)^\s*rule\b", verification)))
)
print(
    "LOCAL_SIMPLIFICATION_COUNT="
    + str(
        len(
            re.findall(
                r"\[(?:[^\]]*,\s*)?simplification(?:\s*,[^\]]*)?\]",
                semantic + verification,
            )
        )
    )
)
print(
    "LOCAL_TOTAL_ATTRIBUTE_COUNT="
    + str(len(re.findall(r"\[(?:[^\]]*,\s*)?total(?:\s*,[^\]]*)?\]", semantic + verification)))
)
print(
    "LOCAL_FUNCTIONAL_ATTRIBUTE_COUNT="
    + str(len(re.findall(r"\[(?:[^\]]*,\s*)?functional(?:\s*,[^\]]*)?\]", semantic + verification)))
)
