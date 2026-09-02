#!/usr/bin/env python3
"""Mutate the actually invoked claim body from space separators to commas."""

from __future__ import annotations

import sys
from pathlib import Path


path = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "/tmp/audit-work/15-string-sequence/candidate-src/stage4-ground.k"
)
text = path.read_text(encoding="utf-8")
text = text.replace("module STAGE4-GROUND", "module STAGE4-BODY-MUTATION")
text = text.replace("[entry-ground-n5]", "[entry-comma-body-n5]")
text = text.replace('Str(" ")', 'Str(",")')
if text.count('Str(",")') != 4:
    # Two occurrences in the loop claim and two in the entry claim: source term
    # plus pinned closure in each. The selected entry therefore invokes comma code.
    raise RuntimeError("unexpected number of mutated program-body literals")
print(text, end="")
