#!/usr/bin/env python3
"""Check that the spec's #loadAll payload is the submitted translated AST."""

from __future__ import annotations

import re
import sys
from pathlib import Path

spec_text = Path("/tmp/audit-work/candidate-src/spec.k").read_text()
submitted = Path("/tmp/audit-work/candidate-src/solution.mpy").read_text()

marker = "#loadAll("
marker_at = spec_text.index(marker)
payload_at = marker_at + len(marker)
depth = 1
in_string = False
escaped = False
end = None
for position in range(payload_at, len(spec_text)):
    char = spec_text[position]
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
            end = position
            break

if end is None:
    raise RuntimeError("unterminated #loadAll payload")

payload = spec_text[payload_at:end]
normalize = lambda text: re.sub(r"\s+", "", text)
same = normalize(payload) == normalize(submitted)
print(f"spec_load_payload_chars={len(payload)}")
print(f"submitted_solution_mpy_chars={len(submitted)}")
print(f"whitespace_normalized_identity={same}")
if not same:
    sys.exit(1)
