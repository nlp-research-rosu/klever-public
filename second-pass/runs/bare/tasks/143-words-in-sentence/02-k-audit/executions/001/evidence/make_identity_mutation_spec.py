#!/usr/bin/env python3
"""Mutate the proved program-identity claim so it must be rejected."""

from __future__ import annotations

from pathlib import Path


BASE = Path("/audit-output/evidence/audit-program-identity.k")
SCRATCH = Path("/tmp/audit-work/rebuild/audit-program-identity-mutation.k")
EVIDENCE = Path("/audit-output/evidence/audit-program-identity-mutation.k")

text = BASE.read_text(encoding="utf-8")
text = text.replace("module AUDIT-PROGRAM-IDENTITY", "module AUDIT-PROGRAM-IDENTITY-MUTATION", 1)
text = text.replace(
    "claim [solution-program-expands-to-regenerated-file]:",
    "claim [solution-program-does-not-expand-to-mutated-file]:",
    1,
)
if text.count("Int(2),") < 1:
    raise RuntimeError("expected Int(2) in generated identity claim")
text = text.replace("Int(2),", "Int(4),", 1)
SCRATCH.write_text(text, encoding="utf-8")
EVIDENCE.write_text(text, encoding="utf-8")
print(f"base={BASE}")
print(f"scratch={SCRATCH}")
print(f"evidence={EVIDENCE}")
print("mutation=first implementation-list Int(2) changed to Int(4)")
