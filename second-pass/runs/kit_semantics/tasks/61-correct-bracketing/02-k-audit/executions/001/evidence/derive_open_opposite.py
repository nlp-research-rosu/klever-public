#!/usr/bin/env python3
"""Derive a second ground value probe from the reviewer-owned false mutation."""

from pathlib import Path

source = Path("/audit-output/evidence/audit-spec-vacuity.k").read_text(
    encoding="utf-8"
)
source = source.replace(
    "module AUDIT-SPEC-VACUITY",
    "module AUDIT-OPEN-OPPOSITE",
).replace(
    "claim [pair-falsely-returns-false]:",
    "claim [open-falsely-returns-true]:",
).replace(
    "str(iCons(40, iCons(41, .IntSeq))))",
    "str(iCons(40, .IntSeq)))",
).replace(
    "      false\n    </k>",
    "      true\n    </k>",
).replace(
    "endmodule",
    "endmodule",
)

if "module AUDIT-OPEN-OPPOSITE" not in source:
    raise SystemExit("module replacement failed")
if "str(iCons(40, .IntSeq))" not in source:
    raise SystemExit("input replacement failed")
if "      true\n    </k>" not in source:
    raise SystemExit("target replacement failed")
print(source, end="")
