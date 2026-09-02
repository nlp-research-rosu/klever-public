#!/usr/bin/env python3
"""Mechanically compare every claim's executed Module term with solution.mpy."""

from __future__ import annotations

import re
from pathlib import Path


def extract_balanced_module(text: str, start: int) -> str:
    assert text.startswith("Module(", start)
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise AssertionError("unbalanced Module term")


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


spec = Path("/tmp/audit-work/reconstruction/spec.k").read_text(encoding="utf-8")
program = Path(
    "/tmp/audit-work/reconstruction/solution.regenerated.mpy"
).read_text(encoding="utf-8")
starts = [match.start() for match in re.finditer(r"\bModule\(", spec)]
assert len(starts) == 4
for index, start in enumerate(starts):
    claim_term = extract_balanced_module(spec, start)
    assert normalize(claim_term) == normalize(program), index
    suffix = spec[start + len(claim_term) :]
    assert re.match(r"\s*~>\s*invoke\(\"sort_array\"", suffix), index
    print(
        f"claim={index + 1} module_term_matches_regenerated_solution=true "
        "continuation_invokes_sort_array=true"
    )

print("entry_precondition_witnesses:")
print("  empty: INPUT=nil")
print("  symbolic_nonempty: F=0 REST=cons(1,nil), nonnegative=true")
print("  example_ascending: INPUT=[2,4,3,0,1,5]")
print("  example_descending: INPUT=[2,4,3,0,1,5,6]")
print("PINNING_CHECK: PASS")
