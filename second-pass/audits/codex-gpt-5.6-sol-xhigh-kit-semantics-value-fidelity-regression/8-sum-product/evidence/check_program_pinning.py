#!/usr/bin/env python3
"""Check that the entry claim's #loadAll argument is the submitted MPY program."""

from __future__ import annotations

import re
from pathlib import Path


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
                return index
    raise ValueError("unbalanced parentheses")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


submitted = Path("/tmp/audit-work/source/solution.mpy").read_text().strip()
spec = Path("/tmp/audit-work/source/spec.k").read_text()
marker = "#loadAll("
marker_index = spec.index(marker)
open_index = marker_index + len(marker) - 1
close_index = matching_paren(spec, open_index)
claimed_program = spec[open_index + 1 : close_index].strip()

print(f"submitted_bytes={len(submitted.encode())}")
print(f"claimed_program_bytes={len(claimed_program.encode())}")
print(f"submitted_compact_chars={len(compact(submitted))}")
print(f"claimed_compact_chars={len(compact(claimed_program))}")
print(f"exact_ignoring_whitespace={compact(submitted) == compact(claimed_program)}")
print(f"loadAll_occurrences={spec.count(marker)}")

assert spec.count(marker) == 1
assert compact(submitted) == compact(claimed_program)
print("REAL_PROGRAM_PINNING=PASS")
