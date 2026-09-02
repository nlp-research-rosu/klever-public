#!/usr/bin/env python3
"""Extract the first entry claim's executed Program term from spec.k."""

from __future__ import annotations

import re
from pathlib import Path


text = Path("/tmp/audit-work/source/spec.k").read_text(encoding="utf-8")
matches = re.findall(
    r"<k>\s*(Module\(.*?)\s*=>\s*\.K\s*</k>",
    text,
    flags=re.DOTALL,
)
if len(matches) != 4:
    raise SystemExit(f"expected four entry claim bodies, found {len(matches)}")

# `.Exprs` is the K unit constructor for the concrete `List{Expr, ","}` syntax.
# In a parsed .mpy source, the same empty list is written by leaving the list
# position empty after Call's required comma.
print(matches[0].replace(".Exprs", ""))
