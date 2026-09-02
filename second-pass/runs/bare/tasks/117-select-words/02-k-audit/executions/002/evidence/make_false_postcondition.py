#!/usr/bin/env python3
"""Create a concrete, satisfiable, false result obligation."""

from __future__ import annotations

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")
source = (SCRATCH / "spec-claim-2.k").read_text()

replacements = {
    "module SPEC-CLAIM-2": "module SPEC-VACUITY",
    '<inputS> "Mary had a little lamb" </inputS>': '<inputS> "b" </inputS>',
    "<inputN> 4 </inputN>": "<inputN> 1 </inputN>",
    'pyList(WCons("little", .Words))': "pyList(.Words)",
}
for old, new in replacements.items():
    if source.count(old) != 1:
        raise SystemExit(f"expected exactly one occurrence of {old!r}")
    source = source.replace(old, new)

target = SCRATCH / "spec-vacuity.k"
target.write_text(source)
print(target)
print("satisfying-witness", repr("b"), "n=1")
print("actual-result", "pyList(WCons(\"b\", .Words))")
print("mutated-required-result", "pyList(.Words)")
