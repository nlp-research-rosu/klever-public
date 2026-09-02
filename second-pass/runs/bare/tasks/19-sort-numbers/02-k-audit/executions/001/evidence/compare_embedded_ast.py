#!/usr/bin/env python3
"""Check that the audit's embedded K term is the submitted solution.mpy term.

Whitespace outside string literals is insignificant K layout and is removed.
Whitespace and escapes inside string literals are preserved.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def compact_k_layout(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            result.append(char)
            in_string = True
        elif not char.isspace():
            result.append(char)
    if in_string:
        raise ValueError("unterminated string")
    compacted = "".join(result)
    # The top-level .mpy parser accepts an omitted zero-length Exprs list after
    # the comma. In a rule RHS, the same list unit must be written `.Exprs`.
    return compacted.replace(",.Exprs)", ",)")


submitted_path = Path("/tmp/audit-work/candidate-src/solution.mpy")
spec_path = Path("/tmp/audit-work/candidate-src/audit-actual-program.k")

submitted = compact_k_layout(submitted_path.read_text())
spec_text = spec_path.read_text()
begin = spec_text.index("// AUDIT_AST_BEGIN") + len("// AUDIT_AST_BEGIN")
end = spec_text.index("// AUDIT_AST_END")
embedded = compact_k_layout(spec_text[begin:end])

print(f"submitted_normalized_sha256={hashlib.sha256(submitted.encode()).hexdigest()}")
print(f"embedded_normalized_sha256={hashlib.sha256(embedded.encode()).hexdigest()}")
print(f"normalized_byte_length={len(submitted.encode())}")
print("normalization=layout plus explicit .Exprs list-unit equivalence")
print(f"identical={submitted == embedded}")
if submitted != embedded:
    raise SystemExit(1)
