#!/usr/bin/env python3
"""Check that the entry claim embeds the trusted-translator output verbatim modulo whitespace."""

from __future__ import annotations

import re
from pathlib import Path


MPY = Path("/tmp/audit-work/78-hex-key/regenerated-solution.mpy")
SPEC = Path("/tmp/audit-work/78-hex-key/candidate-src/spec.k")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    program = MPY.read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")
    start = spec.index("Module(")
    end_marker = "~> #invoke("
    end = spec.index(end_marker, start)
    embedded = spec[start:end]
    same = compact(program) == compact(embedded)
    invokes_submitted_name = '#invoke("hex_key", S:String)' in spec
    claim_has_side_condition = bool(
        re.search(r"^\s+requires\s+(?!\")", spec, flags=re.MULTILINE)
    )

    print(f"regenerated_program={MPY}")
    print(f"entry_spec={SPEC}")
    print(f"program_compact_length={len(compact(program))}")
    print(f"embedded_compact_length={len(compact(embedded))}")
    print(f"embedded_program_matches={same}")
    print(f"invokes_submitted_name={invokes_submitted_name}")
    print(f"claim_has_side_condition={claim_has_side_condition}")
    print(f"universal_input_has_no_side_condition={not claim_has_side_condition}")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
