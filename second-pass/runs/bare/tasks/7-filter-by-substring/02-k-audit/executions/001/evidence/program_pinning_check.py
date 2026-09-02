#!/usr/bin/env python3
"""Check the submitted mpy text against verification.k's solutionProgram RHS."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/7-filter-by-substring")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    verification = (SCRATCH / "verification.k").read_text(encoding="utf-8")
    translated = (SCRATCH / "solution.mpy").read_text(encoding="utf-8")
    match = re.search(
        r"rule\s+solutionProgram\s*=>\s*(Module\(.*?)"
        r"\n\s*syntax\s+PyList\s*::=",
        verification,
        flags=re.DOTALL,
    )
    if match is None:
        print("solutionProgram_rhs_found=false")
        return 1

    rhs = compact(match.group(1))
    mpy = compact(translated)
    print("solutionProgram_rhs_found=true")
    print(f"rhs_compact_sha256={hashlib.sha256(rhs.encode()).hexdigest()}")
    print(f"mpy_compact_sha256={hashlib.sha256(mpy.encode()).hexdigest()}")
    print(f"compact_term_identity={str(rhs == mpy).lower()}")
    print(f"rhs={rhs}")
    print(f"mpy={mpy}")
    return 0 if rhs == mpy else 1


if __name__ == "__main__":
    raise SystemExit(main())
