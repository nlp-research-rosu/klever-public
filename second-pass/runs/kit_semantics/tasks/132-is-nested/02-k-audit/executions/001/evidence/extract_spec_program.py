#!/usr/bin/env python3
"""Extract the Module(...) argument executed by SPEC.program's #loadAll."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SPEC = Path("/candidate/spec.k")


def matching_close(text: str, open_index: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_index, len(text)):
        character = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced parentheses")


text = SPEC.read_text()
program_claim = text.index("claim [program]:")
load_all = text.index("#loadAll(", program_claim)
open_index = text.index("(", load_all)
close_index = matching_close(text, open_index)
module_term = text[open_index + 1 : close_index].strip()
if not module_term.startswith("Module("):
    raise ValueError(f"unexpected #loadAll argument: {module_term[:80]!r}")
identity_count = len(re.findall(r"\.Stmts\b", module_term))
normalized = re.sub(r"\s*\.Stmts\b", "", module_term)
print(
    f"removed_stmts_identity_tokens={identity_count}",
    file=sys.stderr,
)
print(normalized)
