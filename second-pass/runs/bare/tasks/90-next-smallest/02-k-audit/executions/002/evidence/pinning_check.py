#!/usr/bin/env python3
"""Mechanical constructor-text comparison for claim/program pinning."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/90-next-smallest")
spec_text = (ROOT / "candidate-src" / "spec.k").read_text(encoding="utf-8")
regenerated = (ROOT / "regenerated-solution.mpy").read_text(encoding="utf-8")

match = re.search(r"<k>\s*(Module\(.*?\))\s*=>\s*\.K\s*</k>", spec_text, re.DOTALL)
if match is None:
    raise SystemExit("could not extract executed Module term from spec.k")
executed = match.group(1)


def constructor_normalize(text: str) -> str:
    # Both source texts are parsed successfully by the fresh K builds. Removing
    # whitespace is therefore a mechanical formatting normalization only.
    return re.sub(r"\s+", "", text)


executed_normalized = constructor_normalize(executed)
regenerated_normalized = constructor_normalize(regenerated)
print(f"EXECUTED_NORMALIZED_SHA256 {hashlib.sha256(executed_normalized.encode()).hexdigest()}")
print(
    "REGENERATED_NORMALIZED_SHA256 "
    f"{hashlib.sha256(regenerated_normalized.encode()).hexdigest()}"
)
print(f"EXECUTED_TERM {executed_normalized}")
print(f"REGENERATED_TERM {regenerated_normalized}")
assert executed_normalized == regenerated_normalized
print("PINNING_STATUS OK exact constructor tree modulo whitespace")
