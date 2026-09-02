#!/usr/bin/env python3
"""Compare the claim's module term to trusted regenerated solution.mpy."""

from __future__ import annotations

import re
import sys
from pathlib import Path


pinning = Path("/tmp/audit-work/reconstruction/pinning-spec.k").read_text()
regenerated = Path(
    "/tmp/audit-work/reconstruction/regenerated-solution.mpy"
).read_text()
match = re.search(
    r"// BEGIN_REGENERATED_MODULE\s*(.*?)\s*// END_REGENERATED_MODULE",
    pinning,
    flags=re.DOTALL,
)
if match is None:
    raise RuntimeError("pinning constructor markers missing")

embedded = match.group(1)


def constructor_normalize(text: str) -> str:
    # The .mpy constructor language has no string literals containing spaces in
    # this program. The external .mpy parser accepts an omitted empty Stmts list
    # after the If comma; K's inner rule parser requires the explicit identity.
    # Canonicalize only that demonstrated list-syntax sugar, then delete
    # formatting whitespace.
    compact = re.sub(r"\s+", "", text)
    return compact.replace(",)Return(", ",.Stmts)Return(")


print(f"regenerated_constructor_chars={len(constructor_normalize(regenerated))}")
print(f"embedded_constructor_chars={len(constructor_normalize(embedded))}")
identical = constructor_normalize(regenerated) == constructor_normalize(embedded)
print(f"constructor_identity={identical}")
if not identical:
    print("regenerated:", constructor_normalize(regenerated))
    print("embedded:", constructor_normalize(embedded))
sys.exit(0 if identical else 1)
