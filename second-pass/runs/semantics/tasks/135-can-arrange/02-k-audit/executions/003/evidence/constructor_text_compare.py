#!/usr/bin/env python3
"""Compare trusted-regenerated .mpy with the literal used by the pinning claim."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/135-can-arrange")


def normalize(term: str) -> str:
    # The translator prints empty Stmts list arguments as whitespace between
    # commas/parens; K's canonical term spelling is `.Stmts`.
    term = term.replace(".Stmts", "")
    return re.sub(r"\s+", "", term)


def main() -> int:
    regenerated = (ROOT / "regenerated-solution.mpy").read_text()
    pinning = (ROOT / "pinning-spec.k").read_text()
    match = re.search(
        r"<k>\s*solutionProgram\s*=>\s*(Module\(.*?\)\))\s*</k>",
        pinning,
        flags=re.DOTALL,
    )
    if match is None:
        print("PINNING_LITERAL_FOUND: False")
        return 2
    literal = match.group(1)
    normalized_regenerated = normalize(regenerated)
    normalized_literal = normalize(literal)
    print("PINNING_LITERAL_FOUND: True")
    print(f"REGENERATED_NORMALIZED_LENGTH: {len(normalized_regenerated)}")
    print(f"PINNING_NORMALIZED_LENGTH: {len(normalized_literal)}")
    print(f"CONSTRUCTOR_TEXT_MATCH: {normalized_regenerated == normalized_literal}")
    if normalized_regenerated != normalized_literal:
        print(f"REGENERATED: {normalized_regenerated}")
        print(f"PINNING: {normalized_literal}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
