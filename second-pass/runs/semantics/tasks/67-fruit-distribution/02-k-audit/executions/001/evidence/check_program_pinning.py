#!/usr/bin/env python3
"""Compare the submitted MPY Module term to verification.k's loaded Module RHS."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
submitted = (ROOT / "solution.mpy").read_text()
verification = (ROOT / "verification.k").read_text()

match = re.search(
    r"\brule\s+solutionModule\s*=>\s*(Module\(.*\))\s*endmodule\s*$",
    verification,
    re.DOTALL,
)
if match is None:
    raise SystemExit("could not extract solutionModule RHS")
embedded = match.group(1)


def canonical_term(text: str) -> str:
    # The trusted translator pretty-prints the empty Exprs production as an
    # omitted list element (`..., )`), whereas verification.k spells it
    # `.Exprs`. They are the same MPY-SYNTAX term.
    text = text.replace(".Exprs", "")
    text = re.sub(r",\s*\)", ")", text)
    return re.sub(r"\s+", "", text)


submitted_term = canonical_term(submitted)
embedded_term = canonical_term(embedded)
print(f"submitted_normalized_sha256={hashlib.sha256(submitted_term.encode()).hexdigest()}")
print(f"embedded_normalized_sha256={hashlib.sha256(embedded_term.encode()).hexdigest()}")
print(f"normalized_module_terms_identical={submitted_term == embedded_term}")
if submitted_term != embedded_term:
    print(f"submitted={submitted_term}")
    print(f"embedded={embedded_term}")
    raise SystemExit(1)
