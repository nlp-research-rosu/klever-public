#!/usr/bin/env python3
"""Check that verification.k's solutionProgram is the submitted .mpy term."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


MPY = Path("/tmp/audit-work/candidate-src/solution.mpy")
VERIFICATION = Path("/tmp/audit-work/candidate-src/verification.k")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    mpy_text = MPY.read_text(encoding="utf-8")
    verification_text = VERIFICATION.read_text(encoding="utf-8")
    match = re.search(
        r"rule\s+solutionProgram\s*=>\s*(.*?)\n\s*// Independent mathematical contract:",
        verification_text,
        flags=re.DOTALL,
    )
    if match is None:
        raise RuntimeError("could not isolate solutionProgram RHS")
    rhs_text = match.group(1)
    normalized_mpy = compact(mpy_text)
    normalized_rhs = compact(rhs_text)
    result = {
        "submitted_mpy": str(MPY),
        "verification_source": str(VERIFICATION),
        "normalized_submitted": normalized_mpy,
        "normalized_solutionProgram_rhs": normalized_rhs,
        "submitted_sha256": hashlib.sha256(normalized_mpy.encode()).hexdigest(),
        "rhs_sha256": hashlib.sha256(normalized_rhs.encode()).hexdigest(),
        "identical": normalized_mpy == normalized_rhs,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
