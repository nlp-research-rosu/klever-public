#!/usr/bin/env python3
"""Check that verification.k's triangleProgram RHS is the submitted MPY tree."""

from __future__ import annotations

import pathlib
import re


WORK = pathlib.Path("/tmp/audit-work/45-triangle-area")


def compact(text: str) -> str:
    # All string literals in this program contain no whitespace, so this is an
    # unambiguous comparison of the constructor tree's surface representation.
    return re.sub(r"\s+", "", text)


def main() -> None:
    submitted = (WORK / "solution.mpy").read_text(encoding="utf-8")
    verification = (WORK / "verification.k").read_text(encoding="utf-8")
    match = re.search(
        r"rule\s+triangleProgram\s*=>\s*(Module\(.*\))\s*endmodule",
        verification,
        flags=re.DOTALL,
    )
    if match is None:
        raise RuntimeError("could not extract triangleProgram RHS")
    rhs = match.group(1)

    print(f"submitted_compact={compact(submitted)}")
    print(f"triangleProgram_rhs_compact={compact(rhs)}")
    print(f"constructor_tree_identity={compact(submitted) == compact(rhs)}")
    if compact(submitted) != compact(rhs):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
