#!/usr/bin/env python3
"""Bounded full-file scan of the untrusted raw generation transcript."""

from __future__ import annotations

import collections
import hashlib
from pathlib import Path
import re


path = Path("/generation-evidence/codex-output.log")
data = path.read_bytes()
text = data.decode("utf-8", errors="replace")
lines = text.splitlines()
patterns = {
    "#Top": re.compile(r"#Top"),
    "kprove": re.compile(r"\bkprove\b"),
    "kompile": re.compile(r"\bkompile\b"),
    "WarnStuckClaimState": re.compile(r"WarnStuckClaimState"),
    "compiler_error": re.compile(r"\[Error\] Compiler"),
    "prover_error": re.compile(r"\[Error\] Prover"),
    "timeout": re.compile(r"timed out|timeout", re.I),
    "proof_bridge_terms": re.compile(
        r"decimalCodes|oddCountFrom|ODD-OUTER-BODY|priority\(40\)"
    ),
}
print(f"path={path}")
print(f"bytes={len(data)}")
print(f"lines={len(lines)}")
print(f"sha256={hashlib.sha256(data).hexdigest()}")
for name, pattern in patterns.items():
    hits = [number for number, line in enumerate(lines, 1) if pattern.search(line)]
    print(f"{name}_count={len(hits)} first={hits[:10]} last={hits[-10:]}")

selected = [
    (number, line)
    for number, line in enumerate(lines, 1)
    if (
        "#Top" in line
        or "WarnStuckClaimState" in line
        or "[Error] Prover" in line
        or "RESULT:" in line
    )
]
print(f"selected_status_lines={len(selected)}")
for number, line in selected[-200:]:
    # Raw terminal output can contain carriage-return progress updates.
    print(f"{number}: {line[-2000:]}")
