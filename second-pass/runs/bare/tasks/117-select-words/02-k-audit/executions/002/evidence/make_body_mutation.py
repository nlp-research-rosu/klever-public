#!/usr/bin/env python3
"""Mutate the program term inside the symbolic claim, leaving its result fixed."""

from __future__ import annotations

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")
source = (SCRATCH / "spec-claim-1.k").read_text()
source = source.replace("module SPEC-CLAIM-1", "module SPEC-BODY-MUTATION")

needle = 'CmpOp("not in", Str("aeiou"))'
replacement = 'CmpOp("not in", Str("aeio"))'
if source.count(needle) != 1:
    raise SystemExit(f"expected exactly one executed-body occurrence, got {source.count(needle)}")
source = source.replace(needle, replacement)

target = SCRATCH / "spec-body-mutation.k"
target.write_text(source)
print(target)
print("mutation", needle, "=>", replacement)
print("witness", repr("u"), "n=0")
